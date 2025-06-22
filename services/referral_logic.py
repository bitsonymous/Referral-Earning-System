from datetime import datetime
from models.database import get_mongo_db
from routers.websocket import active_connections
from bson import ObjectId


async def distribute_profits(db, txn: dict):
    if txn["amount"] < 1000:
        return

    user_id = txn["user_id"]

    # Level 1
    parent = await db["referrals"].find_one({"child_id": user_id, "level": 1})
    if parent:
        await add_earning(db, txn, parent["parent_id"], 1, 5)

        # Level 2
        grandparent = await db["referrals"].find_one({"child_id": parent["parent_id"], "level": 1})
        if grandparent:
            await add_earning(db, txn, grandparent["parent_id"], 2, 1)


async def add_earning(db, txn: dict, earner_id: str, level: int, percent: float):
    earned_amount = txn["amount"] * percent / 100

    # Insert earning record
    await db["earnings"].insert_one({
        "txn_id": str(txn["_id"]),
        "earner_id": earner_id,
        "source_id": txn["user_id"],
        "level": level,
        "percent": percent,
        "amount": earned_amount,
        "timestamp": datetime.now()
    })

    # Update wallet balance
    await db["users"].update_one(
        {"_id": ObjectId(earner_id)},
        {"$inc": {"wallet": earned_amount}}
    )

    # WebSocket notification
    if earner_id in active_connections:
        try:
            await active_connections[earner_id].send_json({
                "message": "You've earned a new referral bonus!",
                "amount": earned_amount,
                "from_user": txn["user_id"],
                "level": level,
                "txn_id": str(txn["_id"])
            })
        except Exception as e:
            print(f"WebSocket send error to user {earner_id}: {e}")

from fastapi import APIRouter, Depends, HTTPException
from models.database import get_mongo_db
from models.schemas import TransactionCreate
from routers.websocket import active_connections
from bson import ObjectId
import asyncio
from datetime import datetime

router = APIRouter()

@router.post("/purchase")
async def purchase(txn: TransactionCreate, db=Depends(get_mongo_db)):
    if txn.amount < 1000:
        raise HTTPException(status_code=400, detail="Minimum amount is ₹1000")

    txn_doc = {
        "user_id": txn.user_id,
        "amount": txn.amount,
        "timestamp": datetime.utcnow()
    }

    result = await db["transactions"].insert_one(txn_doc)
    txn_id = str(result.inserted_id)

    await distribute_profits(db, txn.user_id, txn.amount, txn_id)

    return {"status": "success", "txn_id": txn_id}


async def distribute_profits(db, user_id: str, amount: float, txn_id: str):
    level = 1
    max_levels = 2
    current_user_id = user_id

    while level <= max_levels:
        referral = await db["referrals"].find_one({"child_id": current_user_id})
        if not referral:
            break

        referrer_id = referral["parent_id"]
        percent = 5.0 if level == 1 else 1.0
        earned_amount = (amount * percent) / 100.0

        # Store earning
        earning_doc = {
            "txn_id": txn_id,
            "earner_id": referrer_id,
            "source_id": user_id,
            "level": level,
            "percent": percent,
            "amount": earned_amount,
            "timestamp": datetime.utcnow()
        }
        await db["earnings"].insert_one(earning_doc)

        # Update wallet
        await db["users"].update_one(
            {"_id": ObjectId(referrer_id)},
            {"$inc": {"wallet": earned_amount}}
        )

        # WebSocket Notification
        if referrer_id in active_connections:
            try:
                await active_connections[referrer_id].send_json({
                    "message": "You've earned a referral bonus!",
                    "amount": earned_amount,
                    "from_user": user_id,
                    "level": level,
                    "txn_id": txn_id
                })
            except Exception as e:
                print(f"[WebSocket] Failed to notify {referrer_id}: {e}")

        current_user_id = referrer_id
        level += 1

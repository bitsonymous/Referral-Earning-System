from fastapi import APIRouter, Depends, HTTPException
from models.database import get_mongo_db
from models.schemas import EarningReportResponse, EarningDetail
from bson import ObjectId

router = APIRouter()

@router.get("/report/{user_id}", response_model=EarningReportResponse)
def get_earning_report(user_id: str, db=Depends(get_mongo_db)):
    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    earnings_collection = db["earnings"]
    transactions_collection = db["transactions"]

    earnings_data = []
    total_earning = 0.0

    earnings = list(earnings_collection.find({"earner_id": user_id}))

    for e in earnings:
        txn = transactions_collection.find_one({"_id": ObjectId(e["txn_id"])})
        if not txn:
            continue

        earnings_data.append(EarningDetail(
            user_id=user_id,
            referred_user_id=txn["user_id"],
            referred_user_txn_id=str(txn["_id"]),
            referred_user_txn_amount=txn["amount"],
            level_earned_from_txn=e["level"],
            amount_earned=e["amount"]
        ))

        total_earning += e["amount"]

    return EarningReportResponse(
        user_id=user_id,
        earnings=earnings_data,
        total_earning=total_earning
    )

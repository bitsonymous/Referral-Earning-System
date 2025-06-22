from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_mongo_db
from models.schemas import UserCreate, UserResponse
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()

# Dummy password hashing function (replace with actual)
def hash_password(password: str) -> str:
    return f"hashed-{password}"


@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate, db=Depends(get_mongo_db)):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user_doc = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "wallet": 0.0,
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }

    result = await db["users"].insert_one(user_doc)
    user_doc["_id"] = str(result.inserted_id)
    return UserResponse(**user_doc)


@router.post("/refer")
async def refer_user(parent_id: str, child_id: str, db=Depends(get_mongo_db)):
    if parent_id == child_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User cannot refer themselves")

    try:
        parent_obj = ObjectId(parent_id)
        child_obj = ObjectId(child_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

    parent = await db["users"].find_one({"_id": parent_obj})
    child = await db["users"].find_one({"_id": child_obj})

    if not parent or not child:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User(s) not found")

    exists = await db["referrals"].find_one({"parent_id": parent_id, "child_id": child_id})
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Referral already exists")

    count = await db["referrals"].count_documents({"parent_id": parent_id, "level": 1})
    if count >= 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent already has 8 direct referrals")

    await db["referrals"].insert_one({
        "parent_id": parent_id,
        "child_id": child_id,
        "level": 1,
        "timestamp": datetime.now(timezone.utc)
    })

    grandparent = await db["referrals"].find_one({"child_id": parent_id, "level": 1})
    if grandparent:
        await db["referrals"].insert_one({
            "parent_id": grandparent["parent_id"],
            "child_id": child_id,
            "level": 2,
            "timestamp": datetime.now(timezone.utc)
        })

    return {"message": "Referral created successfully"}

from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson import ObjectId
from models.database import get_mongo_db
from utils.auth import get_password_hash, verify_password, create_access_token
from models.schemas import UserCreate, UserLogin, Token
from datetime import datetime

router = APIRouter()


@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db=Depends(get_mongo_db)):
    users_collection: Collection = db["users"]

    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_pwd,
        "wallet": 0.0,
        "is_active": True,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(new_user)
    user_id = str(result.inserted_id)

    token = create_access_token(data={"sub": user_id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db=Depends(get_mongo_db)):
    users_collection: Collection = db["users"]

    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}

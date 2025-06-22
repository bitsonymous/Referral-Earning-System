from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# ----------------------
# User Model
# ----------------------
class UserModel(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    wallet: float = 0.0


# ----------------------
# Referral Model
# ----------------------
class ReferralModel(BaseModel):
    parent_id: str  # ObjectId as string
    child_id: str   # ObjectId as string
    level: int


# ----------------------
# Transaction Model
# ----------------------
class TransactionModel(BaseModel):
    user_id: str     # ObjectId as string
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ----------------------
# Earning Model
# ----------------------
class EarningModel(BaseModel):
    txn_id: str       # ObjectId as string
    earner_id: str    # ObjectId as string
    source_id: str    # user who triggered this earning (e.g., buyer)
    level: int
    percent: float
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

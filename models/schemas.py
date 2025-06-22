from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List


# -----------------------
# Auth & User Schemas
# -----------------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_required(cls, v):
        if not v:
            raise ValueError("Password is required")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    email: str
    wallet: float
    is_active: Optional[bool] = True


# -----------------------
# Transactions
# -----------------------

class TransactionCreate(BaseModel):
    user_id: str
    amount: float

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


# -----------------------
# Earnings
# -----------------------

class EarningDetail(BaseModel):
    user_id: str
    referred_user_id: str
    referred_user_txn_id: str
    referred_user_txn_amount: float
    level_earned_from_txn: int
    amount_earned: float

    @field_validator("referred_user_txn_amount", "amount_earned")
    @classmethod
    def amounts_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Amounts must be non-negative")
        return v

    @field_validator("level_earned_from_txn")
    @classmethod
    def level_valid_range(cls, v):
        if v < 1 or v > 8:
            raise ValueError("Level must be between 1 and 8")
        return v


class EarningReportResponse(BaseModel):
    user_id: str
    earnings: List[EarningDetail]
    total_earning: float

    @field_validator("total_earning")
    @classmethod
    def total_earning_non_negative(cls, v):
        if v < 0:
            raise ValueError("Total earning cannot be negative")
        return v

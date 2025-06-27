from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.user

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True

class RewardBase(BaseModel):
    title: str
    source_app: str
    type: str
    value: float
    expiry: Optional[datetime]
    code: Optional[str]
    notes: Optional[str]

class RewardCreate(RewardBase):
    pass

class RewardOut(RewardBase):
    id: int
    owner_id: int
    is_listed: bool
    created_at: datetime
    class Config:
        orm_mode = True

class ListingBase(BaseModel):
    reward_id: int
    price: float
    type: str

class ListingOut(ListingBase):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True

class TransactionOut(BaseModel):
    id: int
    buyer_id: int
    listing_id: int
    amount: float
    commission: float
    created_at: datetime
    class Config:
        orm_mode = True

class WalletOut(BaseModel):
    id: int
    user_id: int
    points: int
    money: float
    class Config:
        orm_mode = True

class CommissionLogOut(BaseModel):
    id: int
    transaction_id: int
    amount: float
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[UserRole] = None

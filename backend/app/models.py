from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Boolean, Enum, Text, func
from sqlalchemy.orm import relationship
from .db import Base
import enum

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.user)
    created_at = Column(DateTime, server_default=func.now())
    rewards = relationship("Reward", back_populates="owner")
    wallet = relationship("Wallet", uselist=False, back_populates="user")

class Reward(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source_app = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(Numeric(10,2), nullable=False)
    expiry = Column(DateTime, nullable=True)
    code = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="rewards")
    is_listed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True, index=True)
    reward_id = Column(Integer, ForeignKey("rewards.id"))
    price = Column(Numeric(10,2), nullable=False)
    type = Column(String, nullable=False)  # free, points, paid
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    listing_id = Column(Integer, ForeignKey("listings.id"))
    amount = Column(Numeric(10,2), nullable=False)
    commission = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    points = Column(Integer, default=0)
    money = Column(Numeric(10,2), default=0)
    user = relationship("User", back_populates="wallet")

class CommissionLog(Base):
    __tablename__ = "commission_logs"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    amount = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

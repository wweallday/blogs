# app/models/user.py

from __future__ import annotations  # Enable forward references
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from datetime import date

if TYPE_CHECKING:
    from models import PurchaseHistory, Wishlist, Review
# Avoid direct imports to prevent circular dependencies
# Instead, use string annotations in type hints

class User(SQLModel, table=True):
    __tablename__ = 'users'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    username: str = Field(
        sa_column=Column(String, index=True, unique=True, nullable=False)
    )
    name: str = Field(
        sa_column=Column(String, nullable=False)
    )
    email: str = Field(
        sa_column=Column(String, index=True, unique=True, nullable=False)
    )
    password_hash: str = Field(
        sa_column=Column(String, nullable=False)
    )
    
    # Relationships using string-based type hints
    purchase_history: List["PurchaseHistory"] = Relationship(back_populates="user")
    wishlist: List["Wishlist"] = Relationship(back_populates="user")
    reviews: List["Review"] = Relationship(back_populates="user")
    
    class Config:
        arbitrary_types_allowed = True

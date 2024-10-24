# app/models/wishlist.py

from __future__ import annotations  # Enable forward references
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey, Date
from datetime import date

if TYPE_CHECKING:
    from models import User,Book

class Wishlist(SQLModel, table=True):
    __tablename__ = 'wishlist'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("users.id"), nullable=False)
    )
    book_id: int = Field(
        sa_column=Column(Integer, ForeignKey("books.id"), nullable=False)
    )
    added_date: date = Field(
        sa_column=Column(Date, default=date.today, nullable=False)
    )
    
    user: Optional["User"] = Relationship(back_populates="wishlist")
    book: Optional["Book"] = Relationship(back_populates="wishlist_entries")
    
    class Config:
        arbitrary_types_allowed = True

# app/models/purchase_history.py

from __future__ import annotations  # Enable forward references
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey

from datetime import date
if TYPE_CHECKING:
    from models import User, Book

# Avoid direct imports to prevent circular dependencies
# Use string-based type hints instead

class PurchaseHistory(SQLModel, table=True):
    __tablename__ = 'purchase_history'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("users.id"), nullable=False)
    )
    book_id: int = Field(
        sa_column=Column(Integer, ForeignKey("books.id"), nullable=False)
    )
    purchase_date: date = Field(
        sa_column=Column(Date, default=date.today, nullable=False)
    )
    price: Optional[float] = Field(
        sa_column=Column(Float, nullable=True)
    )
    location: Optional[str] = Field(
        sa_column=Column(String, nullable=True)
    )
    quantity: int = Field(
        sa_column=Column(Integer, default=1, nullable=False)
    )
    
    # Relationships using string-based type hints
    user: Optional["User"] = Relationship(back_populates="purchase_history")
    book: Optional["Book"] = Relationship(back_populates="purchase_history")
    
    class Config:
        arbitrary_types_allowed = True

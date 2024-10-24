# app/models/review.py

from __future__ import annotations  # Enable forward references
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from datetime import date

if TYPE_CHECKING:
    from models import User, Book

class Review(SQLModel, table=True):
    __tablename__ = 'reviews'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("users.id"), nullable=False)
    )
    book_id: int = Field(
        sa_column=Column(Integer, ForeignKey("books.id"), nullable=False)
    )
    review_text: Optional[str] = Field(
        sa_column=Column(Text, nullable=True)
    )
    rating: int = Field(
        sa_column=Column(Integer, nullable=False)
    )
    review_date: date = Field(
        sa_column=Column(Date, default=date.today, nullable=False)
    )
    
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")
    
    class Config:
        arbitrary_types_allowed = True

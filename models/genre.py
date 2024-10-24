# app/models/genre.py

from __future__ import annotations  # Enable forward references
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String

if TYPE_CHECKING:
    from models import BookGenreLink
    
class Genre(SQLModel, table=True):
    __tablename__ = 'genres'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=Column(String, unique=True, nullable=False)
    )
    
    books: List["BookGenreLink"] = Relationship(back_populates="genre")
    
    class Config:
        arbitrary_types_allowed = True

# app/models/tag.py

from __future__ import annotations  # Enable forward references
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String

if TYPE_CHECKING:
    from models import BookTagLink

class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=Column(String, unique=True, nullable=False)
    )
    
    books: List["BookTagLink"] = Relationship(back_populates="tag")
    
    class Config:
        arbitrary_types_allowed = True

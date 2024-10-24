from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String

if TYPE_CHECKING:
    from models.blogs import Blog
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String, index=True, unique=True, nullable=False))
    name: str = Field(sa_column=Column(String, nullable=False))
    email: str = Field(sa_column=Column(String, index=True, unique=True, nullable=False))
    password_hash: str = Field(sa_column=Column(String, nullable=False))
    
    # Correct Relationship definition
    blogs: List["Blog"] = Relationship(back_populates="author")

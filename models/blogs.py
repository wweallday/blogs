from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime

if TYPE_CHECKING:
    from models.user import User

class Blog(SQLModel, table=True):
    __tablename__ = 'blogs'
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String, nullable=False))
    content: str = Field(sa_column=Column(Text, nullable=False))
    author_id: int = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, 
                                  sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                  sa_column=Column(DateTime, default=datetime.utcnow, 
                                  onupdate=datetime.utcnow))
    
    # Correct Relationship definitions
    author: Optional["User"] = Relationship(back_populates="blogs")
    images: Optional[List["Image"]] = Relationship(
        back_populates="blog",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Image(SQLModel, table=True):
    __tablename__ = 'images'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    blog_id: int = Field(foreign_key="blogs.id", nullable=False)
    image_url: str = Field(sa_column=Column(String, nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    
    # Correct Relationship definition
    blog: Optional["Blog"] = Relationship(back_populates="images")


# app/models/book.py

from __future__ import annotations  # Enable forward references
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Float, Integer, Text, Date, ForeignKey
from datetime import date

if TYPE_CHECKING:
    from models import PurchaseHistory, Genre, Wishlist, Review, Tag

class BookGenreLink(SQLModel, table=True):
    __tablename__ = 'book_genre_links'
    
    book_id: int = Field(
        sa_column=Column(Integer, ForeignKey("books.id"), primary_key=True)
    )
    genre_id: int = Field(
        sa_column=Column(Integer, ForeignKey("genres.id"), primary_key=True)
    )
    
    book: Optional["Book"] = Relationship(back_populates="genres")
    genre: Optional["Genre"] = Relationship(back_populates="books")
    
    class Config:
        arbitrary_types_allowed = True

class BookTagLink(SQLModel, table=True):
    __tablename__ = 'book_tag_links'
    
    book_id: int = Field(
        sa_column=Column(Integer, ForeignKey("books.id"), primary_key=True)
    )
    tag_id: int = Field(
        sa_column=Column(Integer, ForeignKey("tags.id"), primary_key=True)
    )
    
    book: Optional["Book"] = Relationship(back_populates="tags")
    tag: Optional["Tag"] = Relationship(back_populates="books")
    
    class Config:
        arbitrary_types_allowed = True

class Book(SQLModel, table=True):
    __tablename__ = 'books'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    title: str = Field(
        sa_column=Column(String, nullable=False)
    )
    author: str = Field(
        sa_column=Column(String, nullable=False)
    )
    isbn: str = Field(
        sa_column=Column(String, unique=True, nullable=False)
    )
    publication_date: date = Field(
        sa_column=Column(Date, nullable=False)
    )
    publisher: Optional[str] = Field(
        sa_column=Column(String, nullable=True)
    )
    summary: Optional[str] = Field(
        sa_column=Column(Text, nullable=True)
    )
    price: float = Field(
        sa_column=Column(Float, nullable=False)
    )
    stock: int = Field(
        sa_column=Column(Integer, default=0, nullable=False)
    )
    
    genres: List[BookGenreLink] = Relationship(back_populates="book")
    tags: List[BookTagLink] = Relationship(back_populates="book")
    purchase_history: List["PurchaseHistory"] = Relationship(back_populates="book")
    wishlist_entries: List["Wishlist"] = Relationship(back_populates="book")
    reviews: List["Review"] = Relationship(back_populates="book")
    
    class Config:
        arbitrary_types_allowed = True

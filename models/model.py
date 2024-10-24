# from typing import List, Optional
# from sqlmodel import SQLModel, Field, Relationship
# from datetime import date, datetime
# from pydantic import BaseModel
# from sqlalchemy import Column, String, Integer, ForeignKey, TEXT, ARRAY, Date, Float

# # User Model
# class User(SQLModel, table=True):
#     __tablename__ = 'users'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
    
#     username: str = Field(
#         sa_column=Column(String, index=True, unique=True, nullable=False)
#     )
#     name: str = Field(
#         sa_column=Column(String, nullable=False)
#     )
#     email: str = Field(
#         sa_column=Column(String, index=True, unique=True, nullable=False)
#     )
#     password_hash: str = Field(
#         sa_column=Column(String, nullable=False)
#     )
    
#     # Relationships
#     purchase_history: List["PurchaseHistory"] = Relationship(back_populates="user")
#     wishlist: List["Wishlist"] = Relationship(back_populates="user")
#     reviews: List["Review"] = Relationship(back_populates="user")
    
#     class Config:
#         arbitrary_types_allowed = True

# # Genre Model
# class Genre(SQLModel, table=True):
#     __tablename__ = 'genres'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(
#         sa_column=Column(String, index=True, unique=True, nullable=False)
#     )
    
#     books: List["BookGenreLink"] = Relationship(back_populates="genre")

# # BookGenreLink Model
# class BookGenreLink(SQLModel, table=True):
#     __tablename__ = 'book_genre_links'
    
#     book_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("books.id"), primary_key=True)
#     )
#     genre_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("genres.id"), primary_key=True)
#     )
    
#     book: Optional["Book"] = Relationship(back_populates="genres")
#     genre: Optional[Genre] = Relationship(back_populates="books")

# # Tag Model
# class Tag(SQLModel, table=True):
#     __tablename__ = 'tags'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(
#         sa_column=Column(String, index=True, unique=True, nullable=False)
#     )
    
#     books: List["BookTagLink"] = Relationship(back_populates="tag")

# # BookTagLink Model
# class BookTagLink(SQLModel, table=True):
#     __tablename__ = 'book_tag_links'
    
#     book_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("books.id"), primary_key=True)
#     )
#     tag_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("tags.id"), primary_key=True)
#     )
    
#     book: Optional["Book"] = Relationship(back_populates="tags")
#     tag: Optional[Tag] = Relationship(back_populates="books")

# # Book Model
# class Book(SQLModel, table=True):
#     __tablename__ = 'books'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
    
#     title: str = Field(
#         sa_column=Column(String, nullable=False)
#     )
#     author: str = Field(
#         sa_column=Column(String, nullable=False)
#     )
#     isbn: str = Field(
#         sa_column=Column(String, unique=True, nullable=False)
#     )
#     publication_date: date = Field(
#         sa_column=Column(Date, nullable=False)
#     )
#     publisher: Optional[str] = Field(
#         sa_column=Column(String, nullable=True)
#     )
#     summary: Optional[str] = Field(
#         sa_column=Column(TEXT, nullable=True)
#     )
#     price: float = Field(
#         sa_column=Column(Float, nullable=False)
#     )
#     stock: int = Field(
#         sa_column=Column(Integer, default=0, nullable=False)
#     )
    
#     genres: List["BookGenreLink"] = Relationship(back_populates="book")
#     tags: List["BookTagLink"] = Relationship(back_populates="book")
#     purchase_history: List["PurchaseHistory"] = Relationship(back_populates="book")
#     wishlist_entries: List["Wishlist"] = Relationship(back_populates="book")
#     reviews: List["Review"] = Relationship(back_populates="book")
    
#     class Config:
#         arbitrary_types_allowed = True

# # PurchaseHistory Model
# class PurchaseHistory(SQLModel, table=True):
#     __tablename__ = 'purchase_history'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("users.id"), nullable=False)
#     )
#     book_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("books.id"), nullable=False)
#     )
#     purchase_date: date = Field(
#         sa_column=Column(Date, default=date.today, nullable=False)
#     )
#     price: Optional[float] = Field(
#         sa_column=Column(Float, nullable=True)
#     )
#     location: Optional[str] = Field(
#         sa_column=Column(String, nullable=True)
#     )
#     quantity: int = Field(
#         sa_column=Column(Integer, default=1, nullable=False)
#     )
    
#     user: Optional["User"] = Relationship(back_populates="purchase_history")
#     book: Optional["Book"] = Relationship(back_populates="purchase_history")
    
#     class Config:
#         arbitrary_types_allowed = True

# # Wishlist Model
# class Wishlist(SQLModel, table=True):
#     __tablename__ = 'wishlists'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("users.id"), nullable=False)
#     )
#     book_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("books.id"), nullable=False)
#     )
#     added_date: date = Field(
#         sa_column=Column(Date, default=date.today, nullable=False)
#     )
    
#     user: Optional["User"] = Relationship(back_populates="wishlist")
#     book: Optional["Book"] = Relationship(back_populates="wishlist_entries")
    
#     class Config:
#         arbitrary_types_allowed = True

# # Review Model
# class Review(SQLModel, table=True):
#     __tablename__ = 'reviews'
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("users.id"), nullable=False)
#     )
#     book_id: int = Field(
#         sa_column=Column(Integer, ForeignKey("books.id"), nullable=False)
#     )
#     review_text: Optional[str] = Field(
#         sa_column=Column(TEXT, nullable=True)
#     )
#     rating: int = Field(
#         sa_column=Column(Integer, nullable=False)
#     )
#     review_date: date = Field(
#         sa_column=Column(Date, default=date.today, nullable=False)
#     )
    
#     user: Optional["User"] = Relationship(back_populates="reviews")
#     book: Optional["Book"] = Relationship(back_populates="reviews")
    
#     class Config:
#         arbitrary_types_allowed = True

# # Pydantic Models
# class GenreResponse(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True

# class TagResponse(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True

# class BookResponse(BaseModel):
#     id: int
#     title: str
#     author: str
#     isbn: str
#     publication_date: date
#     publisher: Optional[str]
#     summary: Optional[str]
#     price: float
#     stock: int
#     genres: List[GenreResponse] = []
#     tags: List[TagResponse] = []
    
#     class Config:
#         from_attributes = True

# class UserReviewResponse(BaseModel):
#     id: int
#     username: str
#     name: str

#     class Config:
#         from_attributes = True

# class ReviewResponse(BaseModel):
#     id: int
#     user: UserReviewResponse
#     book_id: int
#     review_text: Optional[str]
#     rating: int
#     review_date: date
    
#     class Config:
#         from_attributes = True

# class TokenPayload(BaseModel):
#     sub: Optional[int] = None

# class PurchaseHistoryResponse(BaseModel):
#     book_id: int
#     purchase_date: date
#     price: Optional[float] = None
#     location: Optional[str] = None
#     quantity: int = 1

#     class Config:
#         from_attributes = True

# class WishlistResponse(BaseModel):
#     book_id: int
#     added_date: date

#     class Config:
#         from_attributes = True

# class UserResponse(BaseModel):
#     id: Optional[int]
#     username: str
#     email: str
#     purchase_history: Optional[List[PurchaseHistoryResponse]] = None
#     wishlist: Optional[List[WishlistResponse]] = None
#     reviews: Optional[List[ReviewResponse]] = None

#     class Config:
#         from_attributes = True

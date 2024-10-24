from enum import Enum
# app/schemas/user.py

from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import date


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str

    @validator('username')
    def username_length(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    publication_date: date
    publisher: Optional[str]
    summary: Optional[str]
    price: float
    stock: int
    genres: List[GenreResponse] = []
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


class UserReviewResponse(BaseModel):
    id: int
    username: str
    name: str

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    id: int
    user: UserReviewResponse
    book_id: int
    review_text: Optional[str]
    rating: int
    review_date: date

    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class PurchaseHistoryResponse(BaseModel):
    book_id: int
    purchase_date: date
    price: Optional[float] = None
    location: Optional[str] = None
    quantity: int = 1

    class Config:
        from_attributes = True


class WishlistResponse(BaseModel):
    book_id: int
    added_date: date

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: Optional[int]
    username: str
    email: str
    purchase_history: Optional[List[PurchaseHistoryResponse]] = None
    wishlist: Optional[List[WishlistResponse]] = None
    reviews: Optional[List[ReviewResponse]] = None

    class Config:
        from_attributes = True


class BookType(str, Enum):
    MANGA = "Manga"
    LIGHT_NOVEL = "Light Novel"
    SPECIAL = "Special"
    OTHER = "Other"

#######################################################################################
# books
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    publication_date: date
    publisher: Optional[str] = None
    summary: Optional[str] = None
    price: float
    stock: int = 0

    @validator('price')
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Price must be a positive number')
        return v

    @validator('stock')
    def stock_non_negative(cls, v):
        if v < 0:
            raise ValueError('Stock cannot be negative')
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    publisher: Optional[str] = None
    summary: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    @validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price must be a positive number')
        return v

    @validator('stock')
    def stock_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('Stock cannot be negative')
        return v

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    publication_date: date
    publisher: Optional[str] = None
    summary: Optional[str] = None
    price: float
    stock: int
    genres: List['GenreResponse'] = []
    tags: List['TagResponse'] = []

    class Config:
        from_attributes = True  # Use 'from_attributes' as per your setup

# Genre and Tag Schemas (Assuming they are defined here)
class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Update forward references
BookRead.update_forward_refs()
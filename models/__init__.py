# app/models/__init__.py

from .user import User
from .genre import Genre
from .tag import Tag
from .book import Book, BookGenreLink, BookTagLink
from .purchase_history import PurchaseHistory
from .wishlist import Wishlist
from .review import Review

__all__ = [
    "User",
    "Genre",
    "Tag",
    "Book",
    "BookGenreLink",
    "BookTagLink",
    "PurchaseHistory",
    "Wishlist",
    "Review",
]

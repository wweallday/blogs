# app/repository/book_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.schema import BookCreate, BookUpdate
from fastapi import HTTPException
from models import  Book

async def create_book(db: AsyncSession, book_data: BookCreate):
    book = Book.from_orm(book_data)
    db.add(book)
    try:
        await db.commit()
        await db.refresh(book)
        return book
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating book: {str(e)}")

async def get_book_by_id(db: AsyncSession, book_id: int):
    statement = select(Book).where(Book.id == book_id).options(
        # Include related genres and tags if necessary
    )
    result = await db.execute(statement)
    book = result.scalars().first()
    return book

async def update_book(db: AsyncSession, book_id: int, book_data: BookUpdate):
    book = await get_book_by_id(db, book_id)
    if not book:
        return None
    book_data_dict = book_data.dict(exclude_unset=True)
    for key, value in book_data_dict.items():
        setattr(book, key, value)
    try:
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating book: {str(e)}")

async def delete_book(db: AsyncSession, book_id: int):
    book = await get_book_by_id(db, book_id)
    if not book:
        return None
    try:
        await db.delete(book)
        await db.commit()
        return book
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting book: {str(e)}")

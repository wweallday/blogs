# app/routers/book.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.schema import BookCreate, BookRead, BookUpdate
from repository.books import create_book, get_book_by_id, update_book, delete_book
from core.database_session import get_async_session  # Adjust the import path if necessary

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.post("/", response_model=BookRead, status_code=201)
async def create_book_route(book_data: BookCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        book = await create_book(db, book_data)
        return book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{book_id}", response_model=BookRead)
async def read_book(book_id: int, db: AsyncSession = Depends(get_async_session)):
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookRead)
async def update_book_route(book_id: int, book_data: BookUpdate, db: AsyncSession = Depends(get_async_session)):
    updated_book = await update_book(db, book_id, book_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=204)
async def delete_book_route(book_id: int, db: AsyncSession = Depends(get_async_session)):
    deleted = await delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return

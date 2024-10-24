from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import review_repository
from dependencies import get_db

router = APIRouter()

@router.post("/reviews")
async def create_review(review_data: dict, db: AsyncSession = Depends(get_db)):
    review = await review_repository.create_review(db, review_data)
    return review

@router.get("/reviews/{book_id}")
async def get_reviews_by_book(book_id: int, db: AsyncSession = Depends(get_db)):
    reviews = await review_repository.get_reviews_by_book(db, book_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this book")
    return reviews

@router.put("/reviews/{review_id}")
async def update_review(review_id: int, review_data: dict, db: AsyncSession = Depends(get_db)):
    updated_review = await review_repository.update_review(db, review_id, review_data)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@router.delete("/reviews/{review_id}")
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    deleted_review = await review_repository.delete_review(db, review_id)
    if not deleted_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted"}

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.model import Review

async def create_review(db: AsyncSession, review_data: dict):
    review = Review(**review_data)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

async def get_reviews_by_book(db: AsyncSession, book_id: int):
    statement = select(Review).where(Review.book_id == book_id)
    result = await db.execute(statement)
    return result.scalars().all()

async def update_review(db: AsyncSession, review_id: int, review_data: dict):
    review = await db.get(Review, review_id)
    if not review:
        return None
    for key, value in review_data.items():
        setattr(review, key, value)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

async def delete_review(db: AsyncSession, review_id: int):
    review = await db.get(Review, review_id)
    if not review:
        return None
    await db.delete(review)
    await db.commit()
    return review

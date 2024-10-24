from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import wishlist_repository
from dependencies import get_db

router = APIRouter()

@router.post("/wishlist")
async def add_to_wishlist(wishlist_data: dict, db: AsyncSession = Depends(get_db)):
    wishlist_entry = await wishlist_repository.add_to_wishlist(db, wishlist_data)
    return wishlist_entry

@router.get("/wishlist/{user_id}")
async def get_user_wishlist(user_id: int, db: AsyncSession = Depends(get_db)):
    wishlist = await wishlist_repository.get_wishlist_by_user(db, user_id)
    if not wishlist:
        raise HTTPException(status_code=404, detail="No wishlist entries found for user")
    return wishlist

@router.delete("/wishlist/{wishlist_id}")
async def remove_from_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_db)):
    deleted_wishlist = await wishlist_repository.remove_from_wishlist(db, wishlist_id)
    if not deleted_wishlist:
        raise HTTPException(status_code=404, detail="Wishlist entry not found")
    return {"message": "Wishlist entry deleted"}

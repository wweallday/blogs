from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import purchase_history_repository
from dependencies import get_db

router = APIRouter()

@router.post("/purchase-history")
async def create_purchase_history(purchase_data: dict, db: AsyncSession = Depends(get_db)):
    purchase_history = await purchase_history_repository.create_purchase_history(db, purchase_data)
    return purchase_history

@router.get("/purchase-history/{user_id}")
async def get_user_purchase_history(user_id: int, db: AsyncSession = Depends(get_db)):
    history = await purchase_history_repository.get_purchase_history_by_user(db, user_id)
    if not history:
        raise HTTPException(status_code=404, detail="No purchase history found for user")
    return history

@router.delete("/purchase-history/{history_id}")
async def delete_purchase_history(history_id: int, db: AsyncSession = Depends(get_db)):
    deleted_history = await purchase_history_repository.delete_purchase_history(db, history_id)
    if not deleted_history:
        raise HTTPException(status_code=404, detail="Purchase history not found")
    return {"message": "Purchase history deleted"}

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.model import PurchaseHistory

async def create_purchase_history(db: AsyncSession, purchase_data: dict):
    purchase_history = PurchaseHistory(**purchase_data)
    db.add(purchase_history)
    await db.commit()
    await db.refresh(purchase_history)
    return purchase_history

async def get_purchase_history_by_user(db: AsyncSession, user_id: int):
    statement = select(PurchaseHistory).where(PurchaseHistory.user_id == user_id)
    result = await db.execute(statement)
    return result.scalars().all()

async def delete_purchase_history(db: AsyncSession, history_id: int):
    purchase_history = await db.get(PurchaseHistory, history_id)
    if not purchase_history:
        return None
    await db.delete(purchase_history)
    await db.commit()
    return purchase_history

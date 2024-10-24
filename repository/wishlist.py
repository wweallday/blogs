from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.model import Wishlist

async def add_to_wishlist(db: AsyncSession, wishlist_data: dict):
    wishlist_entry = Wishlist(**wishlist_data)
    db.add(wishlist_entry)
    await db.commit()
    await db.refresh(wishlist_entry)
    return wishlist_entry

async def get_wishlist_by_user(db: AsyncSession, user_id: int):
    statement = select(Wishlist).where(Wishlist.user_id == user_id)
    result = await db.execute(statement)
    return result.scalars().all()

async def remove_from_wishlist(db: AsyncSession, wishlist_id: int):
    wishlist_entry = await db.get(Wishlist, wishlist_id)
    if not wishlist_entry:
        return None
    await db.delete(wishlist_entry)
    await db.commit()
    return wishlist_entry

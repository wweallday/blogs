from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.model import Tag

async def create_tag(db: AsyncSession, tag_data: dict):
    tag = Tag(**tag_data)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag

async def get_tag_by_id(db: AsyncSession, tag_id: int):
    statement = select(Tag).where(Tag.id == tag_id)
    result = await db.execute(statement)
    return result.scalars().first()

async def update_tag(db: AsyncSession, tag_id: int, tag_data: dict):
    tag = await get_tag_by_id(db, tag_id)
    if not tag:
        return None
    for key, value in tag_data.items():
        setattr(tag, key, value)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag

async def delete_tag(db: AsyncSession, tag_id: int):
    tag = await get_tag_by_id(db, tag_id)
    if not tag:
        return None
    await db.delete(tag)
    await db.commit()
    return tag

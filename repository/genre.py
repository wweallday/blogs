from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.model import Genre

async def create_genre(db: AsyncSession, genre_data: dict):
    genre = Genre(**genre_data)
    db.add(genre)
    await db.commit()
    await db.refresh(genre)
    return genre

async def get_genre_by_id(db: AsyncSession, genre_id: int):
    statement = select(Genre).where(Genre.id == genre_id)
    result = await db.execute(statement)
    return result.scalars().first()

async def update_genre(db: AsyncSession, genre_id: int, genre_data: dict):
    genre = await get_genre_by_id(db, genre_id)
    if not genre:
        return None
    for key, value in genre_data.items():
        setattr(genre, key, value)
    db.add(genre)
    await db.commit()
    await db.refresh(genre)
    return genre

async def delete_genre(db: AsyncSession, genre_id: int):
    genre = await get_genre_by_id(db, genre_id)
    if not genre:
        return None
    await db.delete(genre)
    await db.commit()
    return genre

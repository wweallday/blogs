from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import genre_repository
from dependencies import get_db

router = APIRouter()

@router.post("/genres")
async def create_genre(genre_data: dict, db: AsyncSession = Depends(get_db)):
    genre = await genre_repository.create_genre(db, genre_data)
    return genre

@router.get("/genres/{genre_id}")
async def read_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    genre = await genre_repository.get_genre_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@router.put("/genres/{genre_id}")
async def update_genre(genre_id: int, genre_data: dict, db: AsyncSession = Depends(get_db)):
    updated_genre = await genre_repository.update_genre(db, genre_id, genre_data)
    if not updated_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return updated_genre

@router.delete("/genres/{genre_id}")
async def delete_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    deleted_genre = await genre_repository.delete_genre(db, genre_id)
    if not deleted_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return {"message": "Genre deleted"}

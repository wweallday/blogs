from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import tag_repository
from dependencies import get_db

router = APIRouter()

@router.post("/tags")
async def create_tag(tag_data: dict, db: AsyncSession = Depends(get_db)):
    tag = await tag_repository.create_tag(db, tag_data)
    return tag

@router.get("/tags/{tag_id}")
async def read_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    tag = await tag_repository.get_tag_by_id(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.put("/tags/{tag_id}")
async def update_tag(tag_id: int, tag_data: dict, db: AsyncSession = Depends(get_db)):
    updated_tag = await tag_repository.update_tag(db, tag_id, tag_data)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag

@router.delete("/tags/{tag_id}")
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    deleted_tag = await tag_repository.delete_tag(db, tag_id)
    if not deleted_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted"}

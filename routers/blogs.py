# app/routers/blog.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from repository import blogs as blog_repository
from dependencies import get_db, get_current_user
from models.user import User
from models.blogs import Blog
from typing import Optional
from datetime import datetime

router = APIRouter()

# Pydantic Schemas

class ImageCreate(BaseModel):
    image_url: str
    description: Optional[str] = None

class ImageResponse(BaseModel):
    id: int
    image_url: str
    description: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True

class BlogCreate(BaseModel):
    title: str
    content: str

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime
    images: Optional[List[ImageResponse]] = []

    class Config:
        from_attributes = True

# Create a new blog
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_blog = await blog_repository.create_blog(db, blog.title, blog.content, current_user.id)
    return new_blog

# Get all blogs
@router.get("/")
async def read_blogs(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    blogs = await blog_repository.get_all_blogs(db)
    return blogs[skip : skip + limit]

# Get a single blog by ID
@router.get("/{blog_id}")
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await blog_repository.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# Update a blog
@router.put("/{blog_id}")
async def update_blog(blog_id: int, blog_update: BlogUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = await blog_repository.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this blog")
    updated_blog = await blog_repository.update_blog(db, blog_id, blog_update.title, blog_update.content)
    return updated_blog

# Delete a blog
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = await blog_repository.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this blog")
    await blog_repository.delete_blog(db, blog_id)
    return {"succes":"blog delete successful"}

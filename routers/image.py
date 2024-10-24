# app/routers/image.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from repository import blogs as blog_repository
from dependencies import get_db, get_current_user
from datetime import datetime
from models.user import User
from typing import Optional

router = APIRouter()

# Pydantic Schemas

class ImageCreate(BaseModel):
    image_url: str
    description: Optional[str] = None

class ImageUpdate(BaseModel):
    image_url: Optional[str] = None
    description: Optional[str] = None

class ImageResponse(BaseModel):
    id: int
    image_url: str
    description: Optional[str] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def add_image(blog_id: int, file: UploadFile = File(...), description: Optional[str] = None, 
                    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = await blog_repository.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add images to this blog")
    
    # Save the image file to the static/images folder
    file_location = blog_repository.save_image_to_static_folder(file)
    
    new_image = await blog_repository.create_image(db, blog_id, file_location, description)
    return new_image

# Get all images for a blog
@router.get("/", response_model=List[ImageResponse])
async def get_images(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await blog_repository.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    images = await blog_repository.get_images_by_blog(db, blog_id)
    return images

# Update an image
# @router.put("/{image_id}", response_model=ImageResponse)
# async def update_image(blog_id: int, image_id: int, image_update: ImageUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
#     blog = await blog_repository.get_blog(db, blog_id)
#     if not blog:
#         raise HTTPException(status_code=404, detail="Blog not found")
#     if blog.author_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not authorized to update images in this blog")
#     image = await blog_repository.get_image(db, image_id)
#     if not image or image.blog_id != blog_id:
#         raise HTTPException(status_code=404, detail="Image not found in this blog")
#     updated_image = await blog_repository.update_image(db, image_id, image_update.image_url, image_update.description)
#     return updated_image

# Delete an image
@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(blog_id: int, image_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = await blog_repository.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete images from this blog")
    image = await blog_repository.get_image(db, image_id)
    if not image or image.blog_id != blog_id:
        raise HTTPException(status_code=404, detail="Image not found in this blog")
    await blog_repository.delete_image(db, image_id)
    return

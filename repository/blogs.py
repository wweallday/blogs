# app/repository/blog.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, UploadFile
from models.blogs import Blog, Image
from models.user import User
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
import os
# Create a new blog
async def create_blog(db: AsyncSession, title: str, content: str, author_id: int) -> Blog:
    # Check if a blog with the same title already exists
    result = await db.execute(select(Blog).where(Blog.title == title))
    existing_blog = result.scalar()

    if existing_blog:
        raise HTTPException(status_code=400, detail="A blog with this title already exists")

    try:
        blog = Blog(title=title, content=content, author_id=author_id)
        db.add(blog)
        await db.commit()
        await db.refresh(blog)
        return blog
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint error")

# Get a blog by ID
async def get_blog(db: AsyncSession, blog_id: int) -> Optional[Blog]:
    statement = select(Blog).where(Blog.id == blog_id)
    result = await db.execute(statement)
    return result.scalars().first()

# Get all blogs
async def get_all_blogs(db: AsyncSession) -> List[Blog]:
    statement = select(Blog).order_by(Blog.created_at.desc())
    result = await db.execute(statement)
    return result.scalars().all()

# Update a blog
async def update_blog(db: AsyncSession, blog_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Blog]:
    blog = await get_blog(db, blog_id)
    if not blog:
        return None

    # Check if the title is being changed
    if title and title != blog.title:
        # Check if another blog with the same title exists
        result = await db.execute(select(Blog).where(Blog.title == title))
        existing_blog = result.scalar()

        if existing_blog:
            raise HTTPException(status_code=400, detail="A blog with this title already exists")

        # Update the title
        blog.title = title

    # Update content if provided
    if content:
        blog.content = content

    # Save the updated blog
    db.add(blog)
    await db.commit()
    await db.refresh(blog)
    
    return blog

# Delete a blog
async def delete_blog(db: AsyncSession, blog_id: int) -> Optional[Blog]:
    blog = await get_blog(db, blog_id)
    if not blog:
        return None
    await db.delete(blog)
    await db.commit()
    return blog

async def create_image(db: AsyncSession, blog_id: int, image_url: str, description: Optional[str] = None) -> Image:
    try:
        image = Image(blog_id=blog_id, image_url=image_url, description=description)
        db.add(image)
        await db.commit()
        await db.refresh(image)
        return image
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint error")

# Get an image by ID
async def get_image(db: AsyncSession, image_id: int) -> Optional[Image]:
    statement = select(Image).where(Image.id == image_id)
    result = await db.execute(statement)
    return result.scalars().first()

# Get all images for a blog
async def get_images_by_blog(db: AsyncSession, blog_id: int) -> List[Image]:
    statement = select(Image).where(Image.blog_id == blog_id)
    result = await db.execute(statement)
    return result.scalars().all()

# Update an image
async def update_image(db: AsyncSession, image_id: int, image_url: Optional[str] = None, description: Optional[str] = None) -> Optional[Image]:
    image = await get_image(db, image_id)
    if not image:
        return None
    if image_url:
        image.image_url = image_url
    if description:
        image.description = description
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image

# Delete an image
async def delete_image(db: AsyncSession, image_id: int) -> Optional[Image]:
    image = await get_image(db, image_id)
    if not image:
        return None
    await db.delete(image)
    await db.commit()
    return image

def save_image_to_static_folder(file: UploadFile):
    folder_path = 'static/images/'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    file_location = os.path.join(folder_path, file.filename)

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    return file_location

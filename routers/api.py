from fastapi import APIRouter

from routers import (
    user,
    blogs,
    image
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(blogs.router, prefix="/blogs", tags=["blogs"])
api_router.include_router(image.router, prefix="/image", tags=["image"])
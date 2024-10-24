from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.user import User
from passlib.context import CryptContext
from sqlmodel import select
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from config import settings
from sqlalchemy import or_

# For hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create an access token (remains the same)
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Authenticate user credentials (async)
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if user and verify_password(password, user.password_hash):
        return user
    return None

# Utility to verify password (remains the same)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Utility to hash password (remains the same)
def hash_password(password):
    return pwd_context.hash(password)

# Create a new user (async)
async def get_user_by_email_or_username(db: AsyncSession, username: str, email: str):
    statement = select(User).where(
        (User.email == email) | (User.username == username)
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, username: str, email: str, password: str, name: str):
    # Check if user exists
    existing_user = await get_user_by_email_or_username(db, username, email)
    
    if existing_user:
        if existing_user.username == username:
            raise HTTPException(status_code=400, detail="Username is already taken")
        if existing_user.email == email:
            raise HTTPException(status_code=400, detail="Email is already registered")
    
    try:
        # Create new user
        hashed_password = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            name=name
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
        
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Can't create user due to a backend error")

# Get user by username (async)
async def get_user_by_username(db: AsyncSession, username: str):
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)  # Await the async execution
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: int):
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    return result.scalars().first()

async def update_user(db: AsyncSession, user_id: int, user_data: dict):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    await db.delete(user)
    await db.commit()
    return user
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from models.user import User
from models.schema import TokenPayload
from typing import Annotated
from core.database_session import _ASYNC_SESSIONMAKER



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")
TokenDep = Annotated[str, Depends(oauth2_scheme)]
print(TokenDep)
# Create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with _ASYNC_SESSIONMAKER() as session:
        yield session


async def get_current_user(
    token: TokenDep, 
    session: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=403, 
            detail="Invalid token"
        )
    
    # Query by user ID (as stored in sub)
    user = await session.get(User, int(token_data.sub))
    if not user:
        raise HTTPException(
            status_code=404,  
            detail="User not found"
        )
    return user

from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from app.core.config import settings
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User
from app.db.models.token import RefreshToken

async def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

async def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncSession, username_or_email: str, password: str):
    q = select(User).where((User.username == username_or_email) | (User.email == username_or_email))
    r = await db.execute(q)
    user = r.scalar_one_or_none()
    if not user:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded

async def create_refresh_token(db: AsyncSession, user_id: uuid.UUID, token_str: str):
    rt = RefreshToken(user_id=user_id, token=token_str)
    db.add(rt)
    await db.commit()
    return rt

async def revoke_refresh_token(db: AsyncSession, token_str: str):
    q = select(RefreshToken).where(RefreshToken.token == token_str)
    r = await db.execute(q)
    rt = r.scalar_one_or_none()
    if rt:
        rt.revoked = True
        db.add(rt)
        await db.commit()

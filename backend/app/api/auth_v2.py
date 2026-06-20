from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user, create_access_token, create_refresh_token, revoke_refresh_token
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.identity import TokenResponse, UserCreate, UserOut
from app.db.models.user import User
from app.services.auth_service import get_password_hash
import uuid
from sqlalchemy import select

router = APIRouter()

@router.post('/login', response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token({"sub": str(user.id), "role": getattr(user, 'role_id', None)})
    # create a refresh token (simple UUID here)
    refresh_token = str(uuid.uuid4())
    await create_refresh_token(db, user.id, refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post('/logout')
async def logout(refresh_token: str, db: AsyncSession = Depends(get_session)):
    await revoke_refresh_token(db, refresh_token)
    return {"status": "ok"}

@router.post('/refresh', response_model=TokenResponse)
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_session)):
    q = select(RefreshToken).where(RefreshToken.token == refresh_token)
    r = await db.execute(q)
    rt = r.scalar_one_or_none()
    if not rt or rt.revoked:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    access_token = create_access_token({"sub": str(rt.user_id)})
    return {"access_token": access_token}

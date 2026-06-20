from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.dependencies import require_active_user
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.identity import UserCreate, UserOut
from app.db.models.user import User
from app.services.auth_service import get_password_hash
from sqlalchemy import select

router = APIRouter()

@router.post('/', response_model=UserOut)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    hashed = await get_password_hash(payload.password)
    user = User(username=payload.username, email=payload.email, hashed_password=hashed, role_id=payload.role_id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut(id=user.id, username=user.username, email=user.email, is_active=user.is_active, role_id=user.role_id)

@router.get('/', response_model=List[UserOut], dependencies=[Depends(require_active_user)])
async def list_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(User.__table__.select().where(User.is_deleted == False).limit(100))
    rows = result.fetchall()
    return [{"id": r.id, "username": r.username, "email": r.email, "is_active": r.is_active, "role_id": r.role_id} for r in rows]

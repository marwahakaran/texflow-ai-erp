from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.identity import RoleCreate, RoleOut, PermissionCreate, PermissionOut
from app.db.models.role_permission import Role, Permission, role_permissions
from sqlalchemy import select
from app.core.dependencies import require_active_user

router = APIRouter()

@router.post('/roles', response_model=RoleOut, dependencies=[Depends(require_active_user)])
async def create_role(payload: RoleCreate, db: AsyncSession = Depends(get_session)):
    r = Role(name=payload.name, description=payload.description)
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return RoleOut(id=r.id, name=r.name, description=r.description)

@router.get('/roles', response_model=List[RoleOut], dependencies=[Depends(require_active_user)])
async def list_roles(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Role).where(Role.is_deleted == False))
    rows = result.scalars().all()
    return [RoleOut(id=r.id, name=r.name, description=r.description) for r in rows]

@router.post('/permissions', response_model=PermissionOut, dependencies=[Depends(require_active_user)])
async def create_permission(payload: PermissionCreate, db: AsyncSession = Depends(get_session)):
    p = Permission(name=payload.name, description=payload.description)
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return PermissionOut(id=p.id, name=p.name, description=p.description)

@router.get('/permissions', response_model=List[PermissionOut], dependencies=[Depends(require_active_user)])
async def list_permissions(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Permission).where(Permission.is_deleted == False))
    rows = result.scalars().all()
    return [PermissionOut(id=p.id, name=p.name, description=p.description) for p in rows]

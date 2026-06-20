from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.organization import CompanyCreate, CompanyOut, BranchCreate, BranchOut
from app.db.models.organization import Company, Branch
from app.core.dependencies import require_active_user
from sqlalchemy import select

router = APIRouter(prefix='/api/org', tags=['organization'])

@router.post('/companies', response_model=CompanyOut, dependencies=[Depends(require_active_user)])
async def create_company(payload: CompanyCreate, db: AsyncSession = Depends(get_session)):
    c = Company(name=payload.name, code=payload.code)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return CompanyOut(id=c.id, name=c.name, code=c.code)

@router.get('/companies', response_model=List[CompanyOut], dependencies=[Depends(require_active_user)])
async def list_companies(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Company).where(Company.is_deleted == False))
    rows = result.scalars().all()
    return [CompanyOut(id=c.id, name=c.name, code=c.code) for c in rows]

@router.post('/branches', response_model=BranchOut, dependencies=[Depends(require_active_user)])
async def create_branch(payload: BranchCreate, db: AsyncSession = Depends(get_session)):
    b = Branch(company_id=payload.company_id, name=payload.name, address=payload.address)
    db.add(b)
    await db.commit()
    await db.refresh(b)
    return BranchOut(id=b.id, company_id=b.company_id, name=b.name, address=b.address)

@router.get('/branches', response_model=List[BranchOut], dependencies=[Depends(require_active_user)])
async def list_branches(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Branch).where(Branch.is_deleted == False))
    rows = result.scalars().all()
    return [BranchOut(id=b.id, company_id=b.company_id, name=b.name, address=b.address) for b in rows]

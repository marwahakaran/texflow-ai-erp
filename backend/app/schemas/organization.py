from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import date

class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=2)
    code: str = Field(..., min_length=1)

class CompanyOut(CompanyCreate):
    id: uuid.UUID

class BranchCreate(BaseModel):
    company_id: uuid.UUID
    name: str
    address: Optional[str]

class BranchOut(BranchCreate):
    id: uuid.UUID

# Additional schemas for Factory, Department, etc. (omitted for brevity) 

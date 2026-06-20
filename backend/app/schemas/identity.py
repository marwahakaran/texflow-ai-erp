from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import uuid

class RoleCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str]

class RoleOut(RoleCreate):
    id: uuid.UUID

class PermissionCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str]

class PermissionOut(PermissionCreate):
    id: uuid.UUID

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role_id: Optional[uuid.UUID]

class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    role_id: Optional[uuid.UUID]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str]

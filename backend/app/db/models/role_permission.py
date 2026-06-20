import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Table, ForeignKey
from app.db.base import Base
from app.db.mixins import BaseMixin

# association table for role-permission
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    mapped_column('role_id', UUID(as_uuid=True), ForeignKey('role.id'), primary_key=True),
    mapped_column('permission_id', UUID(as_uuid=True), ForeignKey('permission.id'), primary_key=True),
)

class Role(Base, BaseMixin):
    __tablename__ = "role"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

class Permission(Base, BaseMixin):
    __tablename__ = "permission"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

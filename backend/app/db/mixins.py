from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.orm import declared_attr

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default='now()', nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default='now()', onupdate='now()', nullable=False)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class BaseMixin(TimestampMixin, SoftDeleteMixin):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

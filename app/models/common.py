"""Shared Pydantic base models and pagination."""

from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""
    items: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int


class TimestampMixin(BaseModel):
    """Fields present on all database records."""
    created_at: datetime | None = None
    updated_at: datetime | None = None


class IDMixin(BaseModel):
    """UUID primary key."""
    id: UUID

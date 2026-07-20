from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str | None = Field(default=None, max_length=120)
    description: str | None = None
    image_key: str | None = Field(default=None, max_length=255)
    parent_id: UUID | None = None
    sort_order: int = 0
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    slug: str | None = Field(default=None, max_length=120)
    description: str | None = None
    image_key: str | None = Field(default=None, max_length=255)
    parent_id: UUID | None = None
    sort_order: int | None = None
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    parent_id: UUID | None
    name: str
    slug: str
    description: str | None
    image_key: str | None
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
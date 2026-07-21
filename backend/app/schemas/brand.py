from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str | None = Field(default=None, max_length=120)
    description: str | None = None
    logo_key: str | None = Field(default=None, max_length=255)
    display_order: int = 0
    is_active: bool = True


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    slug: str | None = Field(default=None, max_length=120)
    description: str | None = None
    logo_key: str | None = Field(default=None, max_length=255)
    display_order: int | None = None
    is_active: bool | None = None


class BrandResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: str | None
    logo_key: str | None
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
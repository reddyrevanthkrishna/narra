from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VariantTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    display_name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    display_order: int = 0
    is_active: bool = True


class VariantTypeCreate(VariantTypeBase):
    pass


class VariantTypeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    display_name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


class VariantTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    display_name: str
    description: str | None
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
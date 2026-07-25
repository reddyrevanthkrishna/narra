from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VariantOptionBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    display_value: str = Field(..., min_length=1, max_length=50)
    display_order: int = 0
    is_active: bool = True


class VariantOptionCreate(VariantOptionBase):
    pass


class VariantOptionUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    display_value: str | None = Field(default=None, min_length=1, max_length=50)
    display_order: int | None = None
    is_active: bool | None = None


class VariantOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    variant_type_id: UUID
    code: str
    display_value: str
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
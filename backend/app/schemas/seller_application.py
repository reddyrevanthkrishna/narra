from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums import SellerApplicationStatus


class SellerApplicationBase(BaseModel):
    display_name: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    email: EmailStr

    phone: str = Field(
        min_length=5,
        max_length=30,
    )


class SellerApplicationCreate(SellerApplicationBase):
    pass


class SellerApplicationUpdate(BaseModel):
    display_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=5,
        max_length=30,
    )


class SellerApplicationApprove(BaseModel):
    pass


class SellerApplicationReject(BaseModel):
    rejection_reason: str = Field(
        min_length=1,
        max_length=1000,
    )


class SellerApplicationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    user_id: UUID

    status: SellerApplicationStatus

    display_name: str

    description: str | None

    email: EmailStr

    phone: str

    rejection_reason: str | None

    reviewed_by: UUID | None

    created_at: datetime

    updated_at: datetime
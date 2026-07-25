from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.listing import ListingStatus


class ListingCreate(BaseModel):
    product_id: UUID

    variant_option_id: UUID

    quantity: int = Field(
        ge=1,
    )

    price: Decimal = Field(
        gt=0,
    )


class ListingUpdate(BaseModel):
    quantity: int | None = Field(
        default=None,
        ge=1,
    )

    price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    status: ListingStatus | None = None

    is_active: bool | None = None


class ListingResponse(BaseModel):
    id: UUID

    seller_id: UUID

    product_id: UUID

    variant_option_id: UUID

    quantity: int

    price: Decimal

    status: ListingStatus

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
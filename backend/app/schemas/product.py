from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import (
    COLORWAY_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    IMAGE_KEY_MAX_LENGTH,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    SKU_MAX_LENGTH,
)
from app.enums.product import ProductStatus


class ProductBase(BaseModel):
    category_id: UUID
    brand_id: UUID

    name: str = Field(
        min_length=1,
        max_length=NAME_MAX_LENGTH,
    )

    slug: str = Field(
        min_length=1,
        max_length=SLUG_MAX_LENGTH,
    )

    sku: str | None = Field(
        default=None,
        max_length=SKU_MAX_LENGTH,
    )

    colorway: str | None = Field(
        default=None,
        max_length=COLORWAY_MAX_LENGTH,
    )

    retail_price: Decimal | None = None

    release_date: date | None = None

    description: str | None = Field(
        default=None,
        max_length=DESCRIPTION_MAX_LENGTH,
    )

    thumbnail_key: str | None = Field(
        default=None,
        max_length=IMAGE_KEY_MAX_LENGTH,
    )

    status: ProductStatus = ProductStatus.DRAFT

    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: UUID | None = None
    brand_id: UUID | None = None

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=NAME_MAX_LENGTH,
    )

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=SLUG_MAX_LENGTH,
    )

    sku: str | None = Field(
        default=None,
        max_length=SKU_MAX_LENGTH,
    )

    colorway: str | None = Field(
        default=None,
        max_length=COLORWAY_MAX_LENGTH,
    )

    retail_price: Decimal | None = None

    release_date: date | None = None

    description: str | None = Field(
        default=None,
        max_length=DESCRIPTION_MAX_LENGTH,
    )

    thumbnail_key: str | None = Field(
        default=None,
        max_length=IMAGE_KEY_MAX_LENGTH,
    )

    status: ProductStatus | None = None

    is_active: bool | None = None


class ProductResponse(ProductBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )
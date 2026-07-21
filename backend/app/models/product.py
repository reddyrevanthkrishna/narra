from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Numeric,
    String,
    Text,
    true,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    COLORWAY_MAX_LENGTH,
    IMAGE_KEY_MAX_LENGTH,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    SKU_MAX_LENGTH,
)
from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums.product import ProductStatus

if TYPE_CHECKING:
    from app.models.brand import Brand
    from app.models.category import Category


class Product(BaseEntity):
    __tablename__ = "products"

    category_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    brand_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("brands.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH),
        nullable=False,
        index=True,
    )

    slug: Mapped[str] = mapped_column(
        String(SLUG_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )

    sku: Mapped[str | None] = mapped_column(
        String(SKU_MAX_LENGTH),
        nullable=True,
    )

    colorway: Mapped[str | None] = mapped_column(
        String(COLORWAY_MAX_LENGTH),
        nullable=True,
    )

    retail_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    release_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    thumbnail_key: Mapped[str | None] = mapped_column(
        String(IMAGE_KEY_MAX_LENGTH),
        nullable=True,
    )

    status: Mapped[ProductStatus] = mapped_column(
        enum_column(
            ProductStatus,
            name="productstatus",
        ),
        default=ProductStatus.DRAFT,
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=true(),
        nullable=False,
    )

    category: Mapped["Category"] = relationship(
        back_populates="products",
    )

    brand: Mapped["Brand"] = relationship(
        back_populates="products",
    )
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Numeric, true
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums.listing import ListingStatus

if TYPE_CHECKING:
    from app.models.order_item import OrderItem
    from app.models.product import Product
    from app.models.seller import Seller
    from app.models.variant_option import VariantOption


class Listing(BaseEntity):
    __tablename__ = "listings"

    seller_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("sellers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    variant_option_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("variant_options.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        index=True,
    )

    status: Mapped[ListingStatus] = mapped_column(
        enum_column(
            ListingStatus,
            name="listingstatus",
        ),
        default=ListingStatus.ACTIVE,
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=true(),
        nullable=False,
    )

    seller: Mapped["Seller"] = relationship(
        back_populates="listings",
    )

    product: Mapped["Product"] = relationship(
        back_populates="listings",
    )

    variant_option: Mapped["VariantOption"] = relationship(
        back_populates="listings",
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="listing",
    )
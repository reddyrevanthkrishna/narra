from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import PurchaseSource

if TYPE_CHECKING:
    from app.models.listing import Listing
    from app.models.return_item import ReturnItem
    from app.models.seller_order import SellerOrder


class OrderItem(BaseEntity):
    __tablename__ = "order_items"

    seller_order_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("seller_orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    listing_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("listings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    purchase_source: Mapped[PurchaseSource] = mapped_column(
        enum_column(
            PurchaseSource,
            name="purchasesource",
        ),
        nullable=False,
        default=PurchaseSource.LISTING,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    brand_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    seller_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    variant_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    thumbnail: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    listing_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    offer_discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    coupon_discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    platform_discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    final_price_paid: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    shipping_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    tax_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
    )

    seller_order: Mapped["SellerOrder"] = relationship(
        back_populates="order_items",
    )

    listing: Mapped["Listing"] = relationship(
        back_populates="order_items",
    )

    return_item: Mapped["ReturnItem | None"] = relationship(
        back_populates="order_item",
        uselist=False,
    )
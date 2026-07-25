from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import SellerOrderStatus

if TYPE_CHECKING:
    from app.models.buyer_order import BuyerOrder
    from app.models.order_item import OrderItem
    from app.models.payout import Payout
    from app.models.refund import Refund
    from app.models.return import Return
    from app.models.seller import Seller
    from app.models.shipment import Shipment


class SellerOrder(BaseEntity):
    __tablename__ = "seller_orders"

    buyer_order_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("buyer_orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    seller_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("sellers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    status: Mapped[SellerOrderStatus] = mapped_column(
        enum_column(
            SellerOrderStatus,
            name="sellerorderstatus",
        ),
        default=SellerOrderStatus.PENDING_PAYMENT,
        nullable=False,
        index=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    shipping_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    buyer_order: Mapped["BuyerOrder"] = relationship(
        back_populates="seller_orders",
    )

    seller: Mapped["Seller"] = relationship(
        back_populates="seller_orders",
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="seller_order",
        cascade="all, delete-orphan",
    )

    shipment: Mapped["Shipment"] = relationship(
        back_populates="seller_order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    return_request: Mapped["Return"] = relationship(
        back_populates="seller_order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    refund: Mapped["Refund"] = relationship(
        back_populates="seller_order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    payout: Mapped["Payout"] = relationship(
        back_populates="seller_order",
        uselist=False,
        cascade="all, delete-orphan",
    )
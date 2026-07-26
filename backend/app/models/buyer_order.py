from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import OrderStatus

if TYPE_CHECKING:
    from app.models.address_snapshot import AddressSnapshot
    from app.models.payment import Payment
    from app.models.seller_order import SellerOrder
    from app.models.user import User


class BuyerOrder(BaseEntity):
    __tablename__ = "buyer_orders"

    buyer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    order_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[OrderStatus] = mapped_column(
        enum_column(
            OrderStatus,
        ),
        nullable=False,
        default=OrderStatus.PENDING_PAYMENT,
        index=True,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR",
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

    shipping_discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    seller_discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    platform_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    platform_discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    ordered_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    buyer: Mapped["User"] = relationship(
        back_populates="buyer_orders",
    )

    seller_orders: Mapped[list["SellerOrder"]] = relationship(
        back_populates="buyer_order",
        cascade="all, delete-orphan",
    )

    address_snapshot: Mapped["AddressSnapshot"] = relationship(
        back_populates="buyer_order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    payment: Mapped["Payment | None"] = relationship(
        back_populates="buyer_order",
        uselist=False,
        cascade="all, delete-orphan",
    )
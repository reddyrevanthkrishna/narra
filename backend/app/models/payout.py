from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import PayoutStatus

if TYPE_CHECKING:
    from app.models.seller_order import SellerOrder


class Payout(BaseEntity):
    __tablename__ = "payouts"

    seller_order_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("seller_orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[PayoutStatus] = mapped_column(
        enum_column(
            PayoutStatus,
        ),
        nullable=False,
        default=PayoutStatus.PENDING,
        index=True,
    )

    gross_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    marketplace_commission: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    payment_gateway_fee: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    tax_deducted: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    refund_deduction: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    adjustment_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    net_payout: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    payout_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    seller_order: Mapped["SellerOrder"] = relationship(
        back_populates="payout",
    )
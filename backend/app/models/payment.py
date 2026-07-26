from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import PaymentGateway, PaymentMethod, PaymentStatus

if TYPE_CHECKING:
    from app.models.buyer_order import BuyerOrder


class Payment(BaseEntity):
    __tablename__ = "payments"

    buyer_order_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("buyer_orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[PaymentStatus] = mapped_column(
        enum_column(
            PaymentStatus,
        ),
        nullable=False,
        default=PaymentStatus.PENDING,
        index=True,
    )

    gateway: Mapped[PaymentGateway] = mapped_column(
        enum_column(
            PaymentGateway,
        ),
        nullable=False,
        default=PaymentGateway.RAZORPAY,
    )

    payment_method: Mapped[PaymentMethod | None] = mapped_column(
        enum_column(
            PaymentMethod,
        ),
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR",
    )

    gateway_order_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    gateway_payment_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    gateway_transaction_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    gateway_signature: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    gateway_response: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    buyer_order: Mapped["BuyerOrder"] = relationship(
        back_populates="payment",
    )
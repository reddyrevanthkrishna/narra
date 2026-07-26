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
from app.enums import RefundReason, RefundStatus

if TYPE_CHECKING:
    from app.models.return_request import ReturnRequest


class Refund(BaseEntity):
    __tablename__ = "refunds"

    return_request_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("return_requests.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[RefundStatus] = mapped_column(
        enum_column(
            RefundStatus,
        ),
        nullable=False,
        default=RefundStatus.PENDING,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    reason: Mapped[RefundReason] = mapped_column(
        enum_column(
            RefundReason,
        ),
        nullable=False,
        index=True,
    )

    gateway_refund_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    gateway_transaction_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    gateway_response: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    requested_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    return_request: Mapped["ReturnRequest"] = relationship(
        back_populates="refund",
    )
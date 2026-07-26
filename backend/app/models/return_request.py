from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import ReturnStatus

if TYPE_CHECKING:
    from app.models.refund import Refund
    from app.models.return_item import ReturnItem
    from app.models.seller_order import SellerOrder
    from app.models.user import User


class ReturnRequest(BaseEntity):
    __tablename__ = "return_requests"

    seller_order_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("seller_orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[ReturnStatus] = enum_column(
        ReturnStatus,
        nullable=False,
        default=ReturnStatus.REQUESTED,
        index=True,
    )

    approved_by: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    customer_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    seller_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    requested_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    rejected_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    received_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    seller_order: Mapped["SellerOrder"] = relationship(
        back_populates="return_request",
    )

    approver: Mapped["User | None"] = relationship(
        foreign_keys=[approved_by],
    )

    return_items: Mapped[list["ReturnItem"]] = relationship(
        back_populates="return_request",
        cascade="all, delete-orphan",
    )

    refund: Mapped["Refund | None"] = relationship(
        back_populates="return_request",
        uselist=False,
        cascade="all, delete-orphan",
    )
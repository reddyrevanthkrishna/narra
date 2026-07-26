from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import ShipmentStatus

if TYPE_CHECKING:
    from app.models.seller_order import SellerOrder


class Shipment(BaseEntity):
    __tablename__ = "shipments"

    seller_order_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("seller_orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[ShipmentStatus] = mapped_column(
        enum_column(
            ShipmentStatus,
        ),
        nullable=False,
        default=ShipmentStatus.PENDING,
        index=True,
    )

    carrier: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    carrier_tracking_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    tracking_number: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    tracking_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    shipped_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    estimated_delivery_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    delivered_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    delivery_attempted_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    seller_order: Mapped["SellerOrder"] = relationship(
        back_populates="shipment",
    )
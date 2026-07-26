from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums import ReturnReason

if TYPE_CHECKING:
    from app.models.order_item import OrderItem
    from app.models.return_request import ReturnRequest


class ReturnItem(BaseEntity):
    __tablename__ = "return_items"

    return_request_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("return_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    order_item_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("order_items.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    reason: Mapped[ReturnReason] = mapped_column(
        enum_column(
            ReturnReason,
        ),
        nullable=False,
        index=True,
    )

    condition_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    inspection_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    return_request: Mapped["ReturnRequest"] = relationship(
        back_populates="return_items",
    )

    order_item: Mapped["OrderItem"] = relationship(
        back_populates="return_item",
    )
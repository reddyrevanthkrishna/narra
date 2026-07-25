from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums.seller_application_status import SellerApplicationStatus

if TYPE_CHECKING:
    from app.models.seller import Seller
    from app.models.user import User


class SellerApplication(BaseEntity):
    __tablename__ = "seller_applications"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[SellerApplicationStatus] = mapped_column(
        enum_column(
            SellerApplicationStatus,
            name="sellerapplicationstatus",
        ),
        default=SellerApplicationStatus.PENDING,
        server_default=SellerApplicationStatus.PENDING.value,
        nullable=False,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reviewed_by: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        foreign_keys=[user_id],
        back_populates="seller_applications",
    )

    reviewer: Mapped["User | None"] = relationship(
        foreign_keys=[reviewed_by],
    )

    seller: Mapped["Seller | None"] = relationship(
        back_populates="application",
        uselist=False,
    )
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text, true
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import IMAGE_KEY_MAX_LENGTH, NAME_MAX_LENGTH
from app.db.entity import BaseEntity
from app.db.types import enum_column
from app.enums.seller_status import SellerStatus
from app.enums.seller_type import SellerType

if TYPE_CHECKING:
    from app.models.seller_application import SellerApplication
    from app.models.user import User


class Seller(BaseEntity):
    __tablename__ = "sellers"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    application_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("seller_applications.id", ondelete="SET NULL"),
        nullable=True,
    )

    seller_type: Mapped[SellerType] = mapped_column(
        enum_column(
            SellerType,
            name="sellertype",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[SellerStatus] = mapped_column(
        enum_column(
            SellerStatus,
            name="sellerstatus",
        ),
        default=SellerStatus.ACTIVE,
        nullable=False,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    logo_key: Mapped[str | None] = mapped_column(
        String(IMAGE_KEY_MAX_LENGTH),
        nullable=True,
    )

    banner_key: Mapped[str | None] = mapped_column(
        String(IMAGE_KEY_MAX_LENGTH),
        nullable=True,
    )

    support_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    support_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    average_rating: Mapped[float] = mapped_column(
        default=0,
        server_default="0",
        nullable=False,
    )

    total_reviews: Mapped[int] = mapped_column(
        default=0,
        server_default="0",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=true(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="seller",
    )

    application: Mapped["SellerApplication | None"] = relationship(
        foreign_keys=[application_id],
    )
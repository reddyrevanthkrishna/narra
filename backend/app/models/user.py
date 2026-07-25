from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity
from app.enums import UserRole

if TYPE_CHECKING:
    from app.models.buyer_order import BuyerOrder
    from app.models.seller import Seller
    from app.models.seller_application import SellerApplication
    from app.models.user_profile import UserProfile


class User(BaseEntity):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        default=UserRole.USER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    profile: Mapped["UserProfile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    seller: Mapped["Seller | None"] = relationship(
        back_populates="user",
        uselist=False,
    )

    seller_applications: Mapped[list["SellerApplication"]] = relationship(
        back_populates="user",
        foreign_keys="SellerApplication.user_id",
        cascade="all, delete-orphan",
        order_by="SellerApplication.created_at.desc()",
    )

    buyer_orders: Mapped[list["BuyerOrder"]] = relationship(
        back_populates="buyer",
        cascade="all, delete-orphan",
        order_by="BuyerOrder.created_at.desc()",
    )
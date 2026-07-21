from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, Text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import (
    IMAGE_KEY_MAX_LENGTH,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
)
from app.db.entity import BaseEntity

if TYPE_CHECKING:
    from app.models.product import Product


class Brand(BaseEntity):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(SLUG_MAX_LENGTH),
        unique=True,
        index=True,
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

    display_order: Mapped[int] = mapped_column(
        Integer,
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

    products: Mapped[list["Product"]] = relationship(
        back_populates="brand",
    )
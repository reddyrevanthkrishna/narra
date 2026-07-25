from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entity import BaseEntity

if TYPE_CHECKING:
    from app.models.variant_type import VariantType


class VariantOption(BaseEntity):
    __tablename__ = "variant_options"

    __table_args__ = (
        UniqueConstraint(
            "variant_type_id",
            "code",
            name="uq_variant_type_option_code",
        ),
    )

    variant_type_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "variant_types.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    display_value: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
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
        server_default="true",
        nullable=False,
    )

    variant_type: Mapped["VariantType"] = relationship(
        back_populates="variant_options",
    )
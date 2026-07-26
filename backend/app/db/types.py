from __future__ import annotations

from enum import Enum as PyEnum

from sqlalchemy import Enum


def enum_column(
    enum_cls: type[PyEnum],
    *,
    name: str | None = None,
) -> Enum:
    """
    Create a PostgreSQL enum that stores enum values
    instead of enum member names.

    Example:

        class ProductStatus(StrEnum):
            DRAFT = "draft"

        status = mapped_column(
            enum_column(ProductStatus),
            default=ProductStatus.DRAFT,
            nullable=False,
            index=True,
        )

    Database:
        draft

    Python:
        ProductStatus.DRAFT
    """

    return Enum(
        enum_cls,
        values_callable=lambda enum: [member.value for member in enum],
        validate_strings=True,
        name=name or enum_cls.__name__.lower(),
    )
from enum import Enum as PyEnum

from sqlalchemy import Enum


def enum_column(
    enum_cls: type[PyEnum],
    *,
    name: str,
) -> Enum:
    """
    Create a PostgreSQL enum that stores the enum values
    instead of the enum member names.

    Example:

        class ProductStatus(StrEnum):
            DRAFT = "draft"

    Database:
        draft

    Python:
        ProductStatus.DRAFT
    """

    return Enum(
        enum_cls,
        values_callable=lambda enum: [member.value for member in enum],
        validate_strings=True,
        name=name,
    )
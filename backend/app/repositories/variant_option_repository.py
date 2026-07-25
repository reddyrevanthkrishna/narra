from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.variant_option import VariantOption
from app.repositories.base_repository import BaseRepository


class VariantOptionRepository(BaseRepository[VariantOption]):
    def __init__(self):
        super().__init__(VariantOption)

    def get_by_code(
        self,
        db: Session,
        variant_type_id: UUID,
        code: str,
    ) -> VariantOption | None:
        statement = (
            select(VariantOption)
            .where(
                VariantOption.variant_type_id == variant_type_id,
                VariantOption.code == code,
                VariantOption.deleted_at.is_(None),
            )
        )

        return db.scalar(statement)

    def list_by_variant_type(
        self,
        db: Session,
        variant_type_id: UUID,
    ) -> list[VariantOption]:
        statement = (
            select(VariantOption)
            .where(
                VariantOption.variant_type_id == variant_type_id,
                VariantOption.deleted_at.is_(None),
            )
            .order_by(
                VariantOption.display_order,
                VariantOption.display_value,
            )
        )

        return list(db.scalars(statement).all())
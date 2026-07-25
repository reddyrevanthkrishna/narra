from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.variant_type import VariantType
from app.repositories.base_repository import BaseRepository


class VariantTypeRepository(BaseRepository[VariantType]):
    def __init__(self):
        super().__init__(VariantType)

    def get_by_name(
        self,
        db: Session,
        name: str,
    ) -> VariantType | None:
        statement = (
            select(VariantType)
            .where(VariantType.name == name)
        )

        return db.scalar(statement)
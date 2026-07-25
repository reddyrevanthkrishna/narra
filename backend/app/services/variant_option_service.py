from uuid import UUID

from sqlalchemy.orm import Session

from app.models.variant_option import VariantOption
from app.repositories.variant_option_repository import VariantOptionRepository
from app.schemas.variant_option import (
    VariantOptionCreate,
    VariantOptionUpdate,
)
from app.services.base_service import BaseService


class VariantOptionService(BaseService[VariantOption]):
    def __init__(self):
        super().__init__(
            repository=VariantOptionRepository(),
            entity_name="Variant Option",
        )

    def create(
        self,
        db: Session,
        variant_type_id: UUID,
        payload: VariantOptionCreate,
    ) -> VariantOption:
        variant_option = VariantOption(
            variant_type_id=variant_type_id,
            **payload.model_dump(),
        )

        self.repository.create(
            db=db,
            entity=variant_option,
        )

        return self.commit_and_refresh(
            db=db,
            entity=variant_option,
        )

    def update(
        self,
        db: Session,
        variant_option: VariantOption,
        payload: VariantOptionUpdate,
    ) -> VariantOption:
        self.repository.update(
            entity=variant_option,
            **payload.model_dump(exclude_unset=True),
        )

        return self.commit_and_refresh(
            db=db,
            entity=variant_option,
        )

    def get_by_code(
        self,
        db: Session,
        variant_type_id: UUID,
        code: str,
    ) -> VariantOption | None:
        return self.repository.get_by_code(
            db=db,
            variant_type_id=variant_type_id,
            code=code,
        )

    def list_by_variant_type(
        self,
        db: Session,
        variant_type_id: UUID,
    ) -> list[VariantOption]:
        return self.repository.list_by_variant_type(
            db=db,
            variant_type_id=variant_type_id,
        )
from uuid import UUID

from slugify import slugify
from sqlalchemy.orm import Session

from app.models.variant_type import VariantType
from app.repositories.variant_type_repository import VariantTypeRepository
from app.schemas.variant_type import VariantTypeCreate, VariantTypeUpdate
from app.services.base_service import BaseService


class VariantTypeService(BaseService[VariantType]):
    def __init__(self):
        super().__init__(
            repository=VariantTypeRepository(),
            entity_name="Variant Type",
        )

    def create(
        self,
        db: Session,
        payload: VariantTypeCreate,
    ) -> VariantType:
        data = payload.model_dump()

        data["name"] = slugify(data["name"]).replace("-", "_")

        variant_type = VariantType(**data)

        self.repository.create(
            db=db,
            entity=variant_type,
        )

        return self.commit_and_refresh(
            db=db,
            entity=variant_type,
        )

    def update(
        self,
        db: Session,
        variant_type: VariantType,
        payload: VariantTypeUpdate,
    ) -> VariantType:
        data = payload.model_dump(exclude_unset=True)

        if "name" in data:
            data["name"] = slugify(data["name"]).replace("-", "_")

        self.repository.update(
            entity=variant_type,
            **data,
        )

        return self.commit_and_refresh(
            db=db,
            entity=variant_type,
        )

    def soft_delete(
        self,
        db: Session,
        variant_type_id: UUID,
    ) -> None:
        variant_type = self.get_by_id(
            db=db,
            entity_id=variant_type_id,
        )

        self.repository.soft_delete(
            variant_type,
        )

        self.commit(db)

    def get_by_name(
        self,
        db: Session,
        name: str,
    ) -> VariantType | None:
        return self.repository.get_by_name(
            db=db,
            name=slugify(name).replace("-", "_"),
        )
from slugify import slugify
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.repositories.brand_repository import BrandRepository
from app.schemas.brand import BrandCreate, BrandUpdate
from app.services.base_service import BaseService


class BrandService(BaseService[Brand]):
    def __init__(self):
        super().__init__(
            repository=BrandRepository(),
            entity_name="Brand",
        )

    def create(
        self,
        db: Session,
        payload: BrandCreate,
    ) -> Brand:
        data = payload.model_dump()

        if not data.get("slug"):
            data["slug"] = slugify(data["name"])

        brand = Brand(**data)

        self.repository.create(
            db=db,
            entity=brand,
        )

        return self.commit_and_refresh(
            db=db,
            entity=brand,
        )

    def update(
        self,
        db: Session,
        brand: Brand,
        payload: BrandUpdate,
    ) -> Brand:
        data = payload.model_dump(exclude_unset=True)

        if "name" in data and "slug" not in data:
            data["slug"] = slugify(data["name"])

        self.repository.update(
            entity=brand,
            **data,
        )

        return self.commit_and_refresh(
            db=db,
            entity=brand,
        )

    def get_by_slug(
        self,
        db: Session,
        slug: str,
    ) -> Brand | None:
        return self.repository.get_by_slug(
            db=db,
            slug=slug,
        )
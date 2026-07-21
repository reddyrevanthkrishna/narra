from slugify import slugify
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.repositories.brand_repository import BrandRepository
from app.schemas.brand import BrandCreate, BrandUpdate
from app.services.base_service import BaseService


class BrandService(BaseService):
    def __init__(self):
        self.repository = BrandRepository()

    def create(
        self,
        db: Session,
        payload: BrandCreate,
    ) -> Brand:
        data = payload.model_dump()

        if not data.get("slug"):
            data["slug"] = slugify(data["name"])

        brand = self.repository.create(
            db=db,
            obj_in=data,
        )

        return self.commit_and_refresh(db, brand)

    def update(
        self,
        db: Session,
        brand: Brand,
        payload: BrandUpdate,
    ) -> Brand:
        data = payload.model_dump(exclude_unset=True)

        if "name" in data and "slug" not in data:
            data["slug"] = slugify(data["name"])

        brand = self.repository.update(
            db=db,
            db_obj=brand,
            obj_in=data,
        )

        return self.commit_and_refresh(db, brand)

    def get_by_slug(
        self,
        db: Session,
        slug: str,
    ) -> Brand | None:
        return self.repository.get_by_slug(
            db=db,
            slug=slug,
        )
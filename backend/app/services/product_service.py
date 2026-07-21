from slugify import slugify
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.base_service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self):
        super().__init__(
            repository=ProductRepository(),
            entity_name="Product",
        )

    def create(
        self,
        db: Session,
        payload: ProductCreate,
    ) -> Product:
        data = payload.model_dump()

        if not data.get("slug"):
            data["slug"] = slugify(data["name"])

        product = Product(**data)

        self.repository.create(
            db=db,
            entity=product,
        )

        return self.commit_and_refresh(
            db=db,
            entity=product,
        )

    def update(
        self,
        db: Session,
        product: Product,
        payload: ProductUpdate,
    ) -> Product:
        data = payload.model_dump(exclude_unset=True)

        if "name" in data and "slug" not in data:
            data["slug"] = slugify(data["name"])

        self.repository.update(
            entity=product,
            **data,
        )

        return self.commit_and_refresh(
            db=db,
            entity=product,
        )
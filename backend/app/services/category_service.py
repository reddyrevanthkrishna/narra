from uuid import UUID

from fastapi import HTTPException, status
from slugify import slugify
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.base_service import BaseService


class CategoryService(BaseService[Category]):
    def __init__(
        self,
        repository: CategoryRepository | None = None,
    ):
        repository = repository or CategoryRepository()

        super().__init__(
            repository=repository,
            entity_name="Category",
        )

    def create_category(
        self,
        db: Session,
        category_data: CategoryCreate,
    ) -> Category:
        slug = category_data.slug or slugify(category_data.name)

        if self.repository.get_by_slug(db, slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category slug already exists.",
            )

        if category_data.parent_id:
            parent = self.repository.get_by_id(
                db,
                category_data.parent_id,
            )

            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent category not found.",
                )

        category = Category(
            parent_id=category_data.parent_id,
            name=category_data.name,
            slug=slug,
            description=category_data.description,
            image_key=category_data.image_key,
            sort_order=category_data.sort_order,
            is_active=category_data.is_active,
        )

        self.repository.create(
            db,
            category,
        )

        self.commit_and_refresh(
            db,
            category,
        )

        return category

    def get_category(
        self,
        db: Session,
        category_id: UUID,
    ) -> Category:
        return self.get_by_id(
            db,
            category_id,
        )

    def get_categories(
        self,
        db: Session,
    ) -> list[Category]:
        return self.repository.get_all(db)

    def update_category(
        self,
        db: Session,
        category_id: UUID,
        category_data: CategoryUpdate,
    ) -> Category:
        category = self.get_by_id(
            db,
            category_id,
        )

        if category_data.slug:
            existing = self.repository.get_by_slug(
                db,
                category_data.slug,
            )

            if existing and existing.id != category.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category slug already exists.",
                )

        if category_data.parent_id:
            parent = self.repository.get_by_id(
                db,
                category_data.parent_id,
            )

            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent category not found.",
                )

        update_data = category_data.model_dump(
            exclude_unset=True,
        )

        self.repository.update(
            category,
            **update_data,
        )

        self.commit_and_refresh(
            db,
            category,
        )

        return category

    def delete_category(
        self,
        db: Session,
        category_id: UUID,
    ) -> None:
        category = self.get_by_id(
            db,
            category_id,
        )

        self.repository.soft_delete(
            category,
        )

        self.commit(db)
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_by_slug(
        self,
        db: Session,
        slug: str,
    ) -> Category | None:
        statement = (
            select(Category)
            .where(Category.slug == slug)
        )

        return db.scalar(statement)

    def get_root_categories(
        self,
        db: Session,
    ) -> list[Category]:
        statement = (
            select(Category)
            .where(Category.parent_id.is_(None))
            .order_by(
                Category.sort_order,
                Category.name,
            )
        )

        return list(
            db.scalars(statement).all()
        )

    def get_children(
        self,
        db: Session,
        parent_id: UUID,
    ) -> list[Category]:
        statement = (
            select(Category)
            .where(Category.parent_id == parent_id)
            .order_by(
                Category.sort_order,
                Category.name,
            )
        )

        return list(
            db.scalars(statement).all()
        )
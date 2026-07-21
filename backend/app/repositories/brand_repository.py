from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.repositories.base_repository import BaseRepository


class BrandRepository(BaseRepository[Brand]):
    def __init__(self):
        super().__init__(Brand)

    def get_by_slug(
        self,
        db: Session,
        slug: str,
    ) -> Brand | None:
        statement = (
            select(Brand)
            .where(Brand.slug == slug)
        )

        return db.scalar(statement)
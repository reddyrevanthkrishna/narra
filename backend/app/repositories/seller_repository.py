from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.seller import Seller
from app.repositories.base_repository import BaseRepository


class SellerRepository(BaseRepository[Seller]):
    def __init__(self):
        super().__init__(Seller)

    def get_by_user_id(
        self,
        db: Session,
        user_id: UUID,
    ) -> Seller | None:
        statement = (
            select(Seller)
            .where(
                Seller.user_id == user_id,
                Seller.deleted_at.is_(None),
            )
        )

        return db.scalar(statement)
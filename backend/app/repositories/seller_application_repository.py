from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import SellerApplicationStatus
from app.models.seller_application import SellerApplication
from app.repositories.base_repository import BaseRepository


class SellerApplicationRepository(
    BaseRepository[SellerApplication]
):
    def __init__(self):
        super().__init__(SellerApplication)

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[SellerApplication]:
        statement = (
            select(SellerApplication)
            .where(
                SellerApplication.user_id == user_id,
            )
            .order_by(
                SellerApplication.created_at.desc(),
            )
        )

        return list(
            db.scalars(statement).all()
        )

    def get_pending_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> SellerApplication | None:
        statement = (
            select(SellerApplication)
            .where(
                SellerApplication.user_id == user_id,
                SellerApplication.status
                == SellerApplicationStatus.PENDING,
            )
        )

        return db.scalar(statement)

    def get_pending(
        self,
        db: Session,
    ) -> list[SellerApplication]:
        statement = (
            select(SellerApplication)
            .where(
                SellerApplication.status
                == SellerApplicationStatus.PENDING,
            )
            .order_by(
                SellerApplication.created_at.asc(),
            )
        )

        return list(
            db.scalars(statement).all()
        )

    def has_active_application(
        self,
        db: Session,
        user_id: UUID,
    ) -> bool:
        return (
            self.get_pending_by_user(
                db=db,
                user_id=user_id,
            )
            is not None
        )
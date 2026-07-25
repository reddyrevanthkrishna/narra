from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import (
    SellerApplicationStatus,
    SellerStatus,
    SellerType,
)
from app.models.seller import Seller
from app.models.seller_application import SellerApplication
from app.repositories.seller_application_repository import (
    SellerApplicationRepository,
)
from app.services.base_service import BaseService


class SellerApplicationService(
    BaseService[SellerApplication]
):
    def __init__(self):
        super().__init__(
            repository=SellerApplicationRepository(),
            entity_name="Seller application",
        )

    def create_application(
        self,
        *,
        db: Session,
        user_id: UUID,
        data,
    ) -> SellerApplication:
        if self.repository.has_active_application(
            db=db,
            user_id=user_id,
        ):
            raise ValueError(
                "You already have a pending seller application."
            )

        existing_seller = db.scalar(
            select(Seller).where(
                Seller.user_id == user_id,
            )
        )

        if existing_seller is not None:
            raise ValueError(
                "You already have a seller account."
            )

        application = SellerApplication(
            user_id=user_id,
            display_name=data.display_name,
            description=data.description,
            email=data.email,
            phone=data.phone,
        )

        self.repository.create(
            db=db,
            entity=application,
        )

        return self.commit_and_refresh(
            db=db,
            entity=application,
        )

    def approve(
        self,
        *,
        db: Session,
        application: SellerApplication,
        reviewer_id: UUID,
    ) -> SellerApplication:
        if (
            application.status
            != SellerApplicationStatus.PENDING
        ):
            raise ValueError(
                "Application has already been processed."
            )

        application.status = (
            SellerApplicationStatus.APPROVED
        )
        application.reviewed_by = reviewer_id

        seller = Seller(
            user_id=application.user_id,
            application_id=application.id,
            seller_type=SellerType.INDIVIDUAL,
            status=SellerStatus.ACTIVE,
            display_name=application.display_name,
            description=application.description,
            support_email=application.email,
            support_phone=application.phone,
        )

        db.add(seller)

        return self.commit_and_refresh(
            db=db,
            entity=application,
        )

    def reject(
        self,
        *,
        db: Session,
        application: SellerApplication,
        reviewer_id: UUID,
        rejection_reason: str,
    ) -> SellerApplication:
        if (
            application.status
            != SellerApplicationStatus.PENDING
        ):
            raise ValueError(
                "Application has already been processed."
            )

        rejection_reason = rejection_reason.strip()

        if not rejection_reason:
            raise ValueError(
                "Rejection reason is required."
            )

        application.status = (
            SellerApplicationStatus.REJECTED
        )
        application.reviewed_by = reviewer_id
        application.rejection_reason = rejection_reason

        return self.commit_and_refresh(
            db=db,
            entity=application,
        )

    def get_my_applications(
        self,
        *,
        db: Session,
        user_id: UUID,
    ) -> list[SellerApplication]:
        return self.repository.get_by_user(
            db=db,
            user_id=user_id,
        )

    def get_pending_applications(
        self,
        *,
        db: Session,
    ) -> list[SellerApplication]:
        return self.repository.get_pending(
            db=db,
        )
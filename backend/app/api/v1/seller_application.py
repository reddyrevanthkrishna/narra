from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.admin import get_current_admin
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.seller_application import (
    SellerApplicationApprove,
    SellerApplicationCreate,
    SellerApplicationReject,
    SellerApplicationResponse,
)
from app.services.seller_application_service import (
    SellerApplicationService,
)

router = APIRouter(
    prefix="/seller-applications",
    tags=["Seller Applications"],
)

service = SellerApplicationService()


@router.post(
    "",
    response_model=SellerApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    payload: SellerApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.create_application(
            db=db,
            user_id=current_user.id,
            data=payload,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/me",
    response_model=list[SellerApplicationResponse],
)
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_my_applications(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/pending",
    response_model=list[SellerApplicationResponse],
)
def get_pending_applications(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return service.get_pending_applications(
        db=db,
    )


@router.post(
    "/{application_id}/approve",
    response_model=SellerApplicationResponse,
)
def approve_application(
    application_id: UUID,
    _: SellerApplicationApprove,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    application = service.get_by_id(
        db=db,
        entity_id=application_id,
    )

    try:
        return service.approve(
            db=db,
            application=application,
            reviewer_id=current_admin.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/{application_id}/reject",
    response_model=SellerApplicationResponse,
)
def reject_application(
    application_id: UUID,
    payload: SellerApplicationReject,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    application = service.get_by_id(
        db=db,
        entity_id=application_id,
    )

    try:
        return service.reject(
            db=db,
            application=application,
            reviewer_id=current_admin.id,
            rejection_reason=payload.rejection_reason,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
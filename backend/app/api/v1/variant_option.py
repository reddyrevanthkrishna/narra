from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.variant_option import (
    VariantOptionCreate,
    VariantOptionResponse,
    VariantOptionUpdate,
)
from app.services.variant_option_service import VariantOptionService
from app.services.variant_type_service import VariantTypeService

router = APIRouter(
    prefix="/variant-types/{variant_type_id}/options",
    tags=["Variant Options"],
)

variant_type_service = VariantTypeService()
service = VariantOptionService()


@router.post(
    "/",
    response_model=VariantOptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_variant_option(
    variant_type_id: UUID,
    payload: VariantOptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    variant_type_service.get_by_id(
        db=db,
        entity_id=variant_type_id,
    )

    return service.create(
        db=db,
        variant_type_id=variant_type_id,
        payload=payload,
    )


@router.get(
    "/",
    response_model=list[VariantOptionResponse],
)
def list_variant_options(
    variant_type_id: UUID,
    db: Session = Depends(get_db),
):
    variant_type_service.get_by_id(
        db=db,
        entity_id=variant_type_id,
    )

    return service.list_by_variant_type(
        db=db,
        variant_type_id=variant_type_id,
    )


@router.get(
    "/{option_id}",
    response_model=VariantOptionResponse,
)
def get_variant_option(
    variant_type_id: UUID,
    option_id: UUID,
    db: Session = Depends(get_db),
):
    option = service.get_by_id(
        db=db,
        entity_id=option_id,
    )

    if option.variant_type_id != variant_type_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant option not found.",
        )

    return option


@router.put(
    "/{option_id}",
    response_model=VariantOptionResponse,
)
def update_variant_option(
    variant_type_id: UUID,
    option_id: UUID,
    payload: VariantOptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    option = service.get_by_id(
        db=db,
        entity_id=option_id,
    )

    if option.variant_type_id != variant_type_id:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant option not found.",
        )

    return service.update(
        db=db,
        variant_option=option,
        payload=payload,
    )


@router.delete(
    "/{option_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_variant_option(
    variant_type_id: UUID,
    option_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.soft_delete(
        db=db,
        variant_type_id=variant_type_id,
        option_id=option_id,
    )
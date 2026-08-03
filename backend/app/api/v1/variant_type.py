from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.variant_type import (
    VariantTypeCreate,
    VariantTypeResponse,
    VariantTypeUpdate,
)
from app.services.variant_type_service import VariantTypeService

router = APIRouter(
    prefix="/variant-types",
    tags=["Variant Types"],
)

service = VariantTypeService()


@router.post(
    "/",
    response_model=VariantTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_variant_type(
    payload: VariantTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db=db,
        payload=payload,
    )


@router.get(
    "/",
    response_model=list[VariantTypeResponse],
)
def list_variant_types(
    db: Session = Depends(get_db),
):
    return service.repository.get_all(db)


@router.get(
    "/{variant_type_id}",
    response_model=VariantTypeResponse,
)
def get_variant_type(
    variant_type_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_by_id(
        db=db,
        entity_id=variant_type_id,
    )


@router.put(
    "/{variant_type_id}",
    response_model=VariantTypeResponse,
)
def update_variant_type(
    variant_type_id: UUID,
    payload: VariantTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    variant_type = service.get_by_id(
        db=db,
        entity_id=variant_type_id,
    )

    return service.update(
        db=db,
        variant_type=variant_type,
        payload=payload,
    )


@router.delete(
    "/{variant_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_variant_type(
    variant_type_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.soft_delete(
        db=db,
        variant_type_id=variant_type_id,
    )
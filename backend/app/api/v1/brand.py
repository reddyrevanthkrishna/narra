from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.brand import BrandCreate, BrandResponse, BrandUpdate
from app.services.brand_service import BrandService

router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
)

service = BrandService()


@router.post(
    "/",
    response_model=BrandResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_brand(
    payload: BrandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db=db,
        payload=payload,
    )


@router.get(
    "/",
    response_model=list[BrandResponse],
)
def list_brands(
    db: Session = Depends(get_db),
):
    return service.repository.get_all(db)


@router.get(
    "/{brand_id}",
    response_model=BrandResponse,
)
def get_brand(
    brand_id: UUID,
    db: Session = Depends(get_db),
):
    brand = service.get_by_id(
        db=db,
        obj_id=brand_id,
    )

    if brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found.",
        )

    return brand


@router.put(
    "/{brand_id}",
    response_model=BrandResponse,
)
def update_brand(
    brand_id: UUID,
    payload: BrandUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    brand = service.get_by_id(
        db=db,
        obj_id=brand_id,
    )

    if brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found.",
        )

    return service.update(
        db=db,
        brand=brand,
        payload=payload,
    )


@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_brand(
    brand_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    brand = service.get_by_id(
        db=db,
        obj_id=brand_id,
    )

    if brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found.",
        )

    service.repository.soft_delete(
        db=db,
        db_obj=brand,
    )

    db.commit()
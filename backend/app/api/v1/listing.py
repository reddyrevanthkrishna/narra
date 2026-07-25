from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.listing import (
    ListingCreate,
    ListingResponse,
    ListingUpdate,
)
from app.services.listing_service import ListingService

router = APIRouter(
    prefix="/listings",
    tags=["Listings"],
)

service = ListingService()


@router.post(
    "/",
    response_model=ListingResponse,
    status_code=201,
)
def create_listing(
    payload: ListingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db=db,
        current_user=current_user,
        payload=payload,
    )


@router.get(
    "/me",
    response_model=list[ListingResponse],
)
def get_my_listings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_my_listings(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/{listing_id}",
    response_model=ListingResponse,
)
def get_listing(
    listing_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_by_id(
        db=db,
        entity_id=listing_id,
    )


@router.put(
    "/{listing_id}",
    response_model=ListingResponse,
)
def update_listing(
    listing_id: UUID,
    payload: ListingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    listing = service.get_by_id(
        db=db,
        entity_id=listing_id,
    )

    return service.update(
        db=db,
        listing=listing,
        current_user=current_user,
        payload=payload,
    )


@router.get(
    "/products/{product_id}",
    response_model=list[ListingResponse],
)
def get_product_listings(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_product_listings(
        db=db,
        product_id=product_id,
    )


@router.get(
    "/products/{product_id}/variants/{variant_option_id}",
    response_model=list[ListingResponse],
)
def get_variant_listings(
    product_id: UUID,
    variant_option_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_variant_listings(
        db=db,
        product_id=product_id,
        variant_option_id=variant_option_id,
    )
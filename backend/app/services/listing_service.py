from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.listing import ListingStatus
from app.models.listing import Listing
from app.models.user import User
from app.repositories.listing_repository import ListingRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.seller_repository import SellerRepository
from app.repositories.variant_option_repository import VariantOptionRepository
from app.schemas.listing import ListingCreate, ListingUpdate
from app.services.base_service import BaseService


class ListingService(BaseService[Listing]):
    def __init__(self):
        super().__init__(
            repository=ListingRepository(),
            entity_name="Listing",
        )

        self.seller_repository = SellerRepository()
        self.product_repository = ProductRepository()
        self.variant_option_repository = VariantOptionRepository()

    def create(
        self,
        db: Session,
        current_user: User,
        payload: ListingCreate,
    ) -> Listing:
        seller = self.seller_repository.get_by_user_id(
            db=db,
            user_id=current_user.id,
        )

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found.",
            )

        product = self.product_repository.get_by_id(
            db=db,
            entity_id=payload.product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        variant_option = self.variant_option_repository.get_by_id(
            db=db,
            entity_id=payload.variant_option_id,
        )

        if variant_option is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Variant option not found.",
            )

        if product.variant_type_id != variant_option.variant_type_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Variant option does not belong to the product.",
            )

        listing = Listing(
            seller_id=seller.id,
            product_id=payload.product_id,
            variant_option_id=payload.variant_option_id,
            quantity=payload.quantity,
            price=payload.price,
        )

        self.repository.create(
            db=db,
            entity=listing,
        )

        return self.commit_and_refresh(
            db=db,
            entity=listing,
        )

    def update(
        self,
        db: Session,
        listing: Listing,
        current_user: User,
        payload: ListingUpdate,
    ) -> Listing:
        seller = self.seller_repository.get_by_user_id(
            db=db,
            user_id=current_user.id,
        )

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found.",
            )

        if listing.seller_id != seller.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not own this listing.",
            )

        data = payload.model_dump(
            exclude_unset=True,
        )

        self.repository.update(
            entity=listing,
            **data,
        )

        if listing.quantity <= 0:
            listing.quantity = 0
            listing.status = ListingStatus.INACTIVE
            listing.is_active = False
        elif (
            listing.quantity > 0
            and listing.status == ListingStatus.INACTIVE
        ):
            listing.status = ListingStatus.ACTIVE
            listing.is_active = True

        return self.commit_and_refresh(
            db=db,
            entity=listing,
        )

    def get_my_listings(
        self,
        db: Session,
        current_user: User,
    ) -> list[Listing]:
        seller = self.seller_repository.get_by_user_id(
            db=db,
            user_id=current_user.id,
        )

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found.",
            )

        return self.repository.get_by_seller(
            db=db,
            seller_id=seller.id,
        )

    def get_product_listings(
        self,
        db: Session,
        product_id: UUID,
    ) -> list[Listing]:
        return self.repository.get_by_product(
            db=db,
            product_id=product_id,
        )

    def get_variant_listings(
        self,
        db: Session,
        product_id: UUID,
        variant_option_id: UUID,
    ) -> list[Listing]:
        return self.repository.get_active_by_product_variant(
            db=db,
            product_id=product_id,
            variant_option_id=variant_option_id,
        )
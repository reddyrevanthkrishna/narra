from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.listing import ListingStatus
from app.models.listing import Listing
from app.repositories.base_repository import BaseRepository


class ListingRepository(BaseRepository[Listing]):
    def __init__(self):
        super().__init__(Listing)

    def get_by_seller(
        self,
        db: Session,
        seller_id: UUID,
    ) -> list[Listing]:
        statement = (
            select(Listing)
            .where(Listing.seller_id == seller_id)
        )

        return list(
            db.scalars(statement).all()
        )

    def get_by_product(
        self,
        db: Session,
        product_id: UUID,
    ) -> list[Listing]:
        statement = (
            select(Listing)
            .where(
                Listing.product_id == product_id,
                Listing.is_active.is_(True),
                Listing.status == ListingStatus.ACTIVE,
                Listing.quantity > 0,
            )
            .order_by(Listing.price.asc())
        )

        return list(
            db.scalars(statement).all()
        )

    def get_by_variant(
        self,
        db: Session,
        variant_option_id: UUID,
    ) -> list[Listing]:
        statement = (
            select(Listing)
            .where(
                Listing.variant_option_id == variant_option_id,
                Listing.is_active.is_(True),
                Listing.status == ListingStatus.ACTIVE,
                Listing.quantity > 0,
            )
            .order_by(Listing.price.asc())
        )

        return list(
            db.scalars(statement).all()
        )

    def get_active_by_product_variant(
        self,
        db: Session,
        product_id: UUID,
        variant_option_id: UUID,
    ) -> list[Listing]:
        statement = (
            select(Listing)
            .where(
                Listing.product_id == product_id,
                Listing.variant_option_id == variant_option_id,
                Listing.is_active.is_(True),
                Listing.status == ListingStatus.ACTIVE,
                Listing.quantity > 0,
            )
            .order_by(Listing.price.asc())
        )

        return list(
            db.scalars(statement).all()
        )
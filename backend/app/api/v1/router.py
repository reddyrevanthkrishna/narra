from fastapi import APIRouter

from app.api.v1.root import router as root_router
from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router
from app.api.v1.product import router as product_router
from app.api.v1.variant_type import router as variant_type_router
from app.api.v1.variant_option import router as variant_option_router
from app.api.v1.listing import router as listing_router
from app.api.v1.seller_application import (
    router as seller_application_router,
)

from app.api.v1 import auth
from app.api.v1 import brand
from app.api.v1 import category

api_router = APIRouter()

api_router.include_router(root_router)
api_router.include_router(health_router)
api_router.include_router(users_router)

api_router.include_router(auth.router)
api_router.include_router(category.router)
api_router.include_router(brand.router)
api_router.include_router(product_router)

# Marketplace
api_router.include_router(variant_type_router)
api_router.include_router(variant_option_router)
api_router.include_router(listing_router)

# Seller
api_router.include_router(seller_application_router)
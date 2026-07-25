from fastapi import FastAPI

from app.api.routes.root import router as root_router
from app.api.routes.health import router as health_router
from app.api.routes.users import router as users_router
from app.api.routes.product import router as product_router
from app.api.routes.variant_type import router as variant_type_router
from app.api.routes.variant_option import router as variant_option_router
from app.api.routes.listing import router as listing_router
from app.api.routes.seller_application import (
    router as seller_application_router,
)

from app.api.routes import auth
from app.api.routes import brand
from app.api.routes import category

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

app.include_router(root_router)
app.include_router(health_router)
app.include_router(users_router)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(brand.router)
app.include_router(product_router)

# Marketplace
app.include_router(variant_type_router)
app.include_router(variant_option_router)
app.include_router(listing_router)

# Seller
app.include_router(seller_application_router)
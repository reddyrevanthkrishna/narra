from app.api.routes.auth import router as auth_router
from app.api.routes.brand import router as brand_router
from app.api.routes.category import router as category_router
from app.api.routes.product import router as product_router
from app.api.routes.seller_application import (
    router as seller_application_router,
)
from app.api.routes.users import router as user_router
from app.api.routes.variant_option import (
    router as variant_option_router,
)
from app.api.routes.variant_type import (
    router as variant_type_router,
)

__all__ = [
    "auth_router",
    "brand_router",
    "category_router",
    "product_router",
    "seller_application_router",
    "user_router",
    "variant_option_router",
    "variant_type_router",
]
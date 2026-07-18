from fastapi import FastAPI

from app.api.routes.root import router as root_router
from app.api.routes.health import router as health_router

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

app.include_router(root_router)
app.include_router(health_router)
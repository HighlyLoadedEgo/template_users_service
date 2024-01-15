from fastapi import (
    APIRouter,
    FastAPI,
)

from src.application.api.endpoints import common_router
from src.modules.users.endpoints.admin import admin_router
from src.modules.users.endpoints.users import user_routers


def init_endpoints(app: FastAPI) -> None:
    """Initialize the endpoints for the application."""
    main = APIRouter(prefix="/api")

    main.include_router(user_routers)
    main.include_router(admin_router)

    app.include_router(common_router)
    app.include_router(main)

from fastapi import (
    APIRouter,
    FastAPI,
)

from src.application.api.endpoints import common_router
from src.modules.users.endpoints import user_routers


def init_endpoints(app: FastAPI) -> None:
    main = APIRouter(prefix="/api")

    main.include_router(common_router)
    main.include_router(user_routers)

    app.include_router(main)

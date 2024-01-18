from fastapi import (
    APIRouter,
    FastAPI,
)

from src.application.api import endpoints


def init_routers(app: FastAPI) -> None:
    """Initialize the api for the application."""
    main = APIRouter(prefix="/api")

    for router in endpoints.__routers__:
        main.include_router(router)

    app.include_router(main)

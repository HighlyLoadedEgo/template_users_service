from fastapi import APIRouter

common_router = APIRouter(tags=["Healthcheck"])


@common_router.get("/healthcheck", response_model=str)
async def healthcheck():
    return "OK"

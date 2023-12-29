import uvicorn
from fastapi import FastAPI

from src.application.api.config import Settings


def init_app(config: Settings) -> FastAPI:
    app = FastAPI(
        debug=config.app.debug, title=config.app.title, version=config.app.version
    )

    return app


async def run_api(app: FastAPI, config: Settings) -> None:
    uvicorn_config = uvicorn.Config(
        app,
        host=config.api.host,
        port=config.api.port,
    )
    server = uvicorn.Server(uvicorn_config)
    await server.serve()

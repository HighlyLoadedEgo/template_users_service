from src.application.api.config import Settings
from src.application.di.di_builder import build_di
from src.application.endpoints_init import init_endpoints
from src.application.main import (
    init_app,
    run_api,
)
from src.core.utils.config_loader import load_config


async def main() -> None:
    """Main entry point."""
    config = load_config(config_type_model=Settings)

    app = init_app(app_config=config.app)
    build_di(app=app, config=config)
    init_endpoints(app=app)

    await run_api(config=config.server, app=app)

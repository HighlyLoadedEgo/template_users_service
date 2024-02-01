from src.application.api.endpoints.common import common_router
from src.application.api.endpoints.users.admin import admin_router
from src.application.api.endpoints.users.users import user_router

__routers__ = [common_router, admin_router, user_router]

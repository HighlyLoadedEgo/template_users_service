import secrets
from typing import Callable

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)

from src.application.api.config import AppConfig

security = HTTPBasic()


def check_doc_permission(
    app_config: AppConfig,
) -> Callable[[HTTPBasicCredentials], None]:
    def permission_logic(credentials: HTTPBasicCredentials = Depends(security)) -> None:
        if not app_config.local:
            correct_username = secrets.compare_digest(
                credentials.username, app_config.doc_username
            )
            correct_password = secrets.compare_digest(
                credentials.password, app_config.doc_password
            )
            if not (correct_username and correct_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Basic"},
                )

    return permission_logic

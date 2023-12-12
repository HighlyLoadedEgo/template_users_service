from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from pydantic import TypeAdapter

from src.auth.common.jwt import JWTManager
from src.auth.exceptions import AccessDeniedException
from src.auth.schemas import (
    TokenPayload,
    UserPayload,
)


class CheckPermission:
    __payload: TokenPayload | None = None

    def __init__(self, jwt_manager: JWTManager) -> None:
        self._jwt_manager = jwt_manager

    def __call__(
        self,
        permission_list: list[str],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    ) -> "CheckPermission":
        """Check access for permission list."""
        payload = self._jwt_manager.decode_token(token=credentials.credentials)
        if payload.role not in permission_list:
            raise AccessDeniedException()
        self.__payload = payload

        return self

    def get_user_payload(self) -> UserPayload:
        """Get user payload for authentication."""
        user_payload = TypeAdapter(UserPayload).validate_python(
            self.__payload.model_dump()
        )

        return user_payload

from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from pydantic import TypeAdapter

from src.core.auth import Roles
from src.core.auth.common.jwt import JWTManager
from src.core.auth.exceptions import AccessDeniedException
from src.core.auth.schemas import (
    TokenPayload,
    UserPayload,
)
from src.core.auth.stubs import jwt_manager_stub


class CheckPermission:
    __payload: TokenPayload | None = None

    def __init__(self, permission_list: list[Roles] | None = None) -> None:
        self._permission_list = permission_list

    def __call__(
        self,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
        jwt_manager: Annotated[JWTManager, Depends(jwt_manager_stub)],
    ) -> "CheckPermission":
        """Check access for permission list."""
        payload = jwt_manager.decode_token(token=credentials.credentials)
        if self._permission_list:
            if (role := payload.role) not in self._permission_list:
                raise AccessDeniedException(role=role)
        self.__payload = payload

        return self

    def get_user_payload(self) -> UserPayload:
        """Get user payload for authentication."""
        user_payload = TypeAdapter(UserPayload).validate_python(self.__payload)

        return user_payload

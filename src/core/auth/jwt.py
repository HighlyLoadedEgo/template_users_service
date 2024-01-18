import datetime

from jose import (
    JWTError,
    jwt,
)

from src.core.auth.common.jwt import JWTManager
from src.core.auth.config import JWTConfig
from src.core.auth.constants import TokenTypes
from src.core.auth.exceptions import InvalidTokenException
from src.core.auth.schemas import (
    TokenPayload,
    TokensData,
    UserPayload,
)


class JWTManagerImpl(JWTManager):
    def __init__(self, jwt_config: JWTConfig) -> None:
        self._jwt_config = jwt_config

    def encode_token(self, payload: UserPayload) -> TokensData:
        iat = datetime.datetime.now(datetime.UTC)
        copy_payload: dict = payload.model_dump()
        access_jwt = self._generate_token(
            payload=copy_payload,
            iat=iat,
            exp=(
                iat
                + datetime.timedelta(
                    minutes=self._jwt_config.access_token_expire_minutes
                )
            ),
            type_=TokenTypes.ACCESS.value,
        )
        refresh_jwt = self._generate_token(
            payload=copy_payload,
            iat=iat,
            exp=(
                iat
                + datetime.timedelta(
                    minutes=self._jwt_config.refresh_token_expire_minutes
                )
            ),
            type_=TokenTypes.REFRESH.value,
        )

        return TokensData(
            access_token=access_jwt,
            refresh_token=refresh_jwt,
        )

    def refresh_tokens(self, token: str) -> TokensData:
        payload = self.decode_token(token=token)
        if payload.type != TokenTypes.REFRESH:
            raise InvalidTokenException()

        refreshed_tokens = self.encode_token(UserPayload(**payload.model_dump()))
        return refreshed_tokens

    def _generate_token(
        self, payload: dict, iat: datetime.datetime, exp: datetime.datetime, type_: str
    ) -> str:
        payload.update({"iat": iat, "exp": exp, "type": type_})

        return jwt.encode(
            payload, self._jwt_config.private_key, algorithm=self._jwt_config.algorithm
        )

    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(
                token,
                self._jwt_config.public_key,
                algorithms=[self._jwt_config.algorithm],
            )
        except JWTError as err:
            raise InvalidTokenException() from err

        return TokenPayload(**payload)

import datetime

from jose import jwt

from src.auth.common.jwt import JWTManager
from src.auth.config import JWTConfig
from src.auth.constants import TokenTypes
from src.auth.exceptions import InvalidTokenException
from src.auth.schemas import (
    TokenPayload,
    TokensData,
    UserPayload,
)


class JWTManagerImpl(JWTManager):
    def __init__(self, config: JWTConfig) -> None:
        self._config = config

    def encode_token(self, payload: UserPayload) -> TokensData:
        iat = datetime.datetime.now(datetime.UTC)
        copy_payload: dict = payload.model_dump()
        access_jwt = self._generate_token(
            payload=copy_payload,
            iat=iat,
            exp=(
                iat
                + datetime.timedelta(minutes=self._config.access_token_expire_minutes)
            ),
            type_=TokenTypes.ACCESS.value,
        )
        refresh_jwt = self._generate_token(
            payload=copy_payload,
            iat=iat,
            exp=(
                iat
                + datetime.timedelta(minutes=self._config.refresh_token_expire_minutes)
            ),
            type_=TokenTypes.REFRESH.value,
        )

        return TokensData(
            access_token=access_jwt,
            refresh_token=refresh_jwt,
        )

    def refresh_tokens(self, token: str) -> TokensData:
        payload = self.decode_token(token=token)
        if payload.token != TokenTypes.REFRESH:
            raise InvalidTokenException()

        refreshed_tokens = self.encode_token(UserPayload(**payload.model_dump()))
        return refreshed_tokens

    def _generate_token(
        self, payload: dict, iat: datetime.datetime, exp: datetime.datetime, type_: str
    ) -> str:
        payload.update({"iat": iat, "exp": exp, "type": type_})

        return jwt.encode(
            payload, self._config.private_key, algorithm=self._config.algorithm
        )

    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(
                token, self._config.public_key, algorithms=[self._config.algorithm]
            )
        except jwt.JWTError as err:
            raise InvalidTokenException() from err

        return TokenPayload(**payload)

from typing import AsyncGenerator

from src.core.database import DatabaseConfig
from src.core.database.postgres.main import (
    async_session_maker,
    get_engine,
)
from src.modules.users.repos.reader import UserReaderImpl
from src.modules.users.repos.repository import UserRepositoryImpl
from src.modules.users.uow import UserUoW


class UserUoWProvider:
    def __init__(self, config: DatabaseConfig) -> None:
        self._session_maker = async_session_maker(
            async_engine=get_engine(config=config, async_=True)  # type: ignore
        )

    async def user_uow(self) -> AsyncGenerator[UserUoW, None]:
        async with self._session_maker.begin() as session:
            yield UserUoW(
                session=session,
                user_repository=UserRepositoryImpl,
                user_reader=UserReaderImpl,
            )

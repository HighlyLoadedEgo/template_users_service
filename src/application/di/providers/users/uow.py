from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from src.modules.users.repos.reader import UserReaderImpl
from src.modules.users.repos.repository import UserRepositoryImpl
from src.modules.users.uow import UserUoW


class UserUoWProvider:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def user_uow(self) -> AsyncGenerator[UserUoW, None]:
        async with self._session_maker.begin() as session:
            yield UserUoW(
                session=session,
                user_repository=UserRepositoryImpl,
                user_reader=UserReaderImpl,
            )

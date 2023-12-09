from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.exceptions import (
    CommitErrorException,
    RollbackErrorException,
)


class SqlAlchemyUow:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def get_session(self) -> AsyncSession:
        return self._session

    async def __aenter__(self) -> "SqlAlchemyUow":
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitErrorException() from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackErrorException() from err

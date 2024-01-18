import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_pupu(client, async_session: AsyncSession) -> None:
    from sqlalchemy import select

    from src.modules.users.models import Users

    async_session.add(
        Users(username="string", hashed_password="we", email="qwe", role="eqw")
    )
    async_session.add(
        Users(username="string1", hashed_password="we", email="qwe1", role="eqw")
    )
    await async_session.flush()
    a = await async_session.execute(select(Users))

    assert len(list(a)) == 2

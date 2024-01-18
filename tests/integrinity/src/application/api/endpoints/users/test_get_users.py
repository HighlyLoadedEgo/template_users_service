import logging

import pytest


@pytest.mark.asyncio
async def test_get_users(users_factory, client):
    batch_size = 10
    users = users_factory.create_batch(size=batch_size)
    logging.warning(users)
    response = client.get("/api/users")

    assert response.status_code == 200

    json_data = response.json()
    result = json_data.get("result")

    assert result.get("total") == batch_size
    assert result.get("users") == 1

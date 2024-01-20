from src.core.auth import Roles
from src.core.database.postgres.constants import SortOrder


def test_get_users(users_factory, client):
    batch_size = 20
    users_factory.create_batch(size=batch_size)

    offset = 0
    limit = batch_size
    order = SortOrder.ASC.value

    response = client.get(
        "/api/users", params={"offset": offset, "limit": limit, "order": order}
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert result.get("total") == batch_size
    assert len(result.get("users")) == batch_size
    assert result.get("limit") == limit
    assert result.get("offset") == offset
    assert result.get("order") == order


def test_get_users_pagination(users_factory, client, async_session):
    batch_size = 20
    users_factory.create_batch(size=batch_size)

    offset = 0
    limit = 10
    order = SortOrder.ASC.value

    response = client.get(
        "/api/users", params={"offset": offset, "limit": limit, "order": order}
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert result.get("total") == batch_size
    assert len(result.get("users")) == batch_size // 2
    assert result.get("limit") == limit
    assert result.get("offset") == offset
    assert result.get("order") == order


def test_get_users_with_filters(users_factory, client):
    batch_size = 19
    test_username = "Tester"
    test_role = Roles.ADMIN.value
    is_deleted = False
    users_factory.create(username=test_username, role=test_role, is_deleted=is_deleted)
    users_factory.create_batch(size=batch_size)
    batch_size += 1

    offset = 0
    limit = batch_size
    order = SortOrder.ASC.value

    response = client.get(
        "/api/users",
        params={
            "username": test_username,
            "deleted": is_deleted,
            "role": test_role,
            "offset": offset,
            "limit": limit,
            "order": order,
        },
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert result.get("total") == batch_size
    assert len(result.get("users")) == 1
    assert result.get("limit") == limit
    assert result.get("offset") == offset
    assert result.get("order") == order

    response_user = result.get("users")[0]

    assert response_user.get("username") == test_username
    assert response_user.get("role") == test_role
    assert response_user.get("is_deleted") == is_deleted


def test_get_no_one_users_with_filters(users_factory, client):
    batch_size = 20
    test_is_deleted = False
    users_factory.create_batch(size=batch_size, is_deleted=True)

    offset = 0
    limit = batch_size
    order = SortOrder.ASC.value

    response = client.get(
        "/api/users",
        params={
            "deleted": test_is_deleted,
            "offset": offset,
            "limit": limit,
            "order": order,
        },
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert result.get("total") == batch_size
    assert len(result.get("users")) == 0
    assert result.get("limit") == limit
    assert result.get("offset") == offset
    assert result.get("order") == order

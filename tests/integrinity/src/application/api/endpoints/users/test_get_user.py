import uuid

from src.modules.users.exceptions import UserDoesNotExistException


def test_get_user_by_id(users_factory, client):
    batch_size = 10
    test_user_id = str(uuid.uuid4())
    users_factory.create(id=test_user_id)
    users_factory.create_batch(size=batch_size)

    response = client.get(f"/api/users/{test_user_id}")

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert result.get("id") == test_user_id


def test_user_not_found_by_id(users_factory, client):
    batch_size = 10
    test_user_id = str(uuid.uuid4())
    users_factory.create_batch(size=batch_size)

    response = client.get(f"/api/users/{test_user_id}")

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 404

    error_data = json_data.get("error")

    assert error_data.get("message") == UserDoesNotExistException(test_user_id).message
    assert error_data.get("data").get("search_data") == test_user_id

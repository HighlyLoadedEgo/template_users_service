import logging

from src.modules.users.exceptions import IncorrectUserCredentialsException
from src.modules.users.utils import generate_password_hash


def test_correct_login(users_factory, client):
    test_username = "test_username"
    test_password = "<PASSWORD>"
    test_hashed_password = generate_password_hash(password=test_password)
    users_factory.create(hashed_password=test_hashed_password, username=test_username)

    response = client.post(
        "/api/users/login", json={"username": test_username, "password": test_password}
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert "access_token" in result
    assert "refresh_token" in result
    assert json_data.get("message") is None


def test_incorrect_login(users_factory, client):
    test_username = "test_username"
    test_password = "<PASSWORD>"

    users_factory.create_batch(size=10)

    response = client.post(
        "/api/users/login",
        json={"username": test_username, "password": test_password},
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 401

    error_data = json_data.get("error")

    assert error_data.get("message") == IncorrectUserCredentialsException().message
    logging.warning(error_data)

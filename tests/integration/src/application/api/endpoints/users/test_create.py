from sqlalchemy import (
    func,
    select,
)


def test_create_user(client, sync_session):
    username = "test_user"
    password = "test_password"
    email = "test_email@mail.com"
    phone = "71111111111"

    response = client.post(
        "/api/users",
        json={
            "username": username,
            "password": password,
            "email": email,
            "phone": phone,
        },
    )

    assert response.status_code == 201

    json_data = response.json()

    assert json_data.get("status") == 201
    assert json_data.get("result") is None

    users_count_in_db = sync_session.scalar(select(func.count(1)))

    assert users_count_in_db == 1


def test_create_user_with_conflict_value(client, sync_session, users_factory):
    username = "test_user"
    password = "test_password"
    email = "test_email@mail.com"
    phone = "71111111111"
    users_factory.create(username=username)

    response = client.post(
        "/api/users",
        json={
            "username": username,
            "password": password,
            "email": email,
            "phone": phone,
        },
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 409

    error_data = json_data.get("error")

    assert error_data.get("message") == "User with 'username' is already registered!"
    assert error_data.get("data").get("attribute") == "username"

    users_count_in_db = sync_session.scalar(select(func.count(1)))

    assert users_count_in_db == 1

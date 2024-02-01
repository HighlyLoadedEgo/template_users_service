from sqlalchemy import select

from src.modules.users.models import Users


def test_update_all_user_updatable_fields(
    test_user, access_auth_headers, client, sync_session
):
    new_username = "new_username"
    new_email = "new_email@mail.com"
    new_phone = "71111111111"

    response = client.patch(
        "/api/users",
        headers=access_auth_headers,
        json={"username": new_username, "email": new_email, "phone": new_phone},
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200
    assert json_data.get("result") is None

    user_from_db = sync_session.scalar(select(Users).where(Users.id == test_user.id))

    assert user_from_db.id == test_user.id
    assert user_from_db.username == new_username
    assert user_from_db.email == new_email
    assert user_from_db.phone == new_phone


def test_update_all_user_one_field(
    test_user, access_auth_headers, client, sync_session
):
    new_username = "new_username"

    response = client.patch(
        "/api/users", headers=access_auth_headers, json={"username": new_username}
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200
    assert json_data.get("result") is None

    user_from_db = sync_session.scalar(select(Users).where(Users.id == test_user.id))

    assert user_from_db.id == test_user.id
    assert user_from_db.username == new_username
    assert user_from_db.email == test_user.email
    assert user_from_db.phone == test_user.phone


def test_not_auth_update(client):
    response = client.patch("/api/users")

    assert response.status_code == 403

    json_data = response.json()

    assert json_data.get("detail") == "Not authenticated"

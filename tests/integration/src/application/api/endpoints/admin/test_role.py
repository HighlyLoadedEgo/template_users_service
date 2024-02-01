import uuid

from sqlalchemy import select

from src.core.auth import Roles
from src.modules.users.exceptions import UserDoesNotExistException
from src.modules.users.models import Users


def test_update_user_role(access_auth_headers, client, sync_session, users_factory):
    new_user = users_factory.create()

    response = client.patch(
        "/api/admin/users/role/",
        headers=access_auth_headers,
        json={"role": Roles.ADMIN.value, "user_id": str(new_user.id)},
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200
    assert json_data.get("result") is None

    user_from_db = sync_session.scalar(select(Users).where(Users.id == new_user.id))
    sync_session.refresh(user_from_db)

    assert user_from_db.role == Roles.ADMIN


def test_not_auth_update_user_role(access_auth_headers, client):
    test_uncreated_user_id = uuid.uuid4()

    response = client.patch(
        "/api/admin/users/role/",
        headers=access_auth_headers,
        json={"role": Roles.ADMIN, "user_id": str(test_uncreated_user_id)},
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 404

    error_data = json_data.get("error")

    assert (
        error_data.get("message")
        == UserDoesNotExistException(test_uncreated_user_id).message
    )
    assert error_data.get("data").get("search_data") == str(test_uncreated_user_id)

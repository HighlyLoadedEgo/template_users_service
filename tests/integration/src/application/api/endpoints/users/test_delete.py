import pytest
from sqlalchemy import select

from src.modules.users.models import Users


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_delete_user(test_user, access_auth_headers, client, sync_session):
    response = client.delete(
        "/api/users",
        headers=access_auth_headers,
    )

    assert response.status_code == 204
    assert response.read() == b""

    user_from_db = sync_session.scalar(select(Users).where(Users.id == test_user.id))

    assert user_from_db.id == test_user.id
    assert user_from_db.is_deleted is True


def test_not_auth_delete_user(client):
    response = client.delete("/api/users")

    assert response.status_code == 403

    json_data = response.json()

    assert json_data.get("detail") == "Not authenticated"

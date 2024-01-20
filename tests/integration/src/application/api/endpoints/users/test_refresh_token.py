import pytest

from src.core.auth.constants import TokenTypes
from src.core.auth.exceptions import InvalidTokenException


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_correct_refresh_token(client, jwt_manager, test_user):
    token = jwt_manager._generate_token(
        payload=dict(id=str(test_user.id), role=test_user.role),
        type_=TokenTypes.REFRESH.value,
    )
    auth_headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/users/refresh_token",
        headers=auth_headers,
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert "access_token" in result
    assert "refresh_token" in result
    assert json_data.get("message") is None


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_incorrect_refresh_token(access_auth_headers, client):
    response = client.post(
        "/api/users/refresh_token",
        headers=access_auth_headers,
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 401

    error_data = json_data.get("error")

    assert error_data.get("message") == InvalidTokenException().message

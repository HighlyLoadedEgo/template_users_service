from src.core.auth import UserPayload
from src.core.auth.exceptions import InvalidTokenException


def test_correct_refresh_token(client, jwt_manager, test_user):
    token = jwt_manager.encode_token(
        payload=UserPayload(id=str(test_user.id), role=test_user.role),
    )
    auth_headers = {"Authorization": f"Bearer {token.refresh_token}"}

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

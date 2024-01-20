import pytest


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_profile(test_user, access_auth_headers, client):
    response = client.get(
        "/api/users/profile/",
        headers=access_auth_headers,
    )

    assert response.status_code == 200

    json_data = response.json()

    assert json_data.get("status") == 200

    result = json_data.get("result")

    assert result.get("id") == str(test_user.id)


def test_not_auth_profile(client):
    response = client.get("/api/users/profile/")

    assert response.status_code == 403

    json_data = response.json()

    assert json_data.get("detail") == "Not authenticated"

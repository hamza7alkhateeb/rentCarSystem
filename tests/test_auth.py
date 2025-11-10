import pytest

from tests.conftest import api_client,create_user
@pytest.mark.django_db
def test_register_user(api_client):
    data = {"username": "hamza", "password": "1234","confirm_password":"1234"}
    response = api_client.post("/api/auth/register/", data)
    assert response.status_code == 201
    assert "message"in response.data
    assert response.data["message"] == "User registered successfully!"

@pytest.mark.django_db
def test_login_user(api_client, create_user):
    create_user(username="hamza", password="1234")
    response = api_client.post("/api/auth/login/", {"username": "hamza", "password": "1234"})
    assert response.status_code == 200
    assert "access" in response.data
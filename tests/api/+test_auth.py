import pytest
from utils.api_client import APIClient
from tests.constants import LOGIN_ENDPOINT


class TestAuth:

    def test_login_existing_user(self, test_user):
        data = {"email": test_user["email"], "password": test_user["password"]}
        response = APIClient.post(LOGIN_ENDPOINT, data)
        assert response.status_code == 200
        assert "accessToken" in response.json()

    def test_login_invalid_credentials(self):
        data = {"email": "wrong@example.com", "password": "wrongpass"}
        response = APIClient.post(LOGIN_ENDPOINT, data)
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"

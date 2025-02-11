import pytest
from utils.api_client import APIClient
from tests.constants import REGISTER_ENDPOINT
from utils.data_generator import generate_user


class TestUser:

    def test_create_unique_user1(self, test_user):
        response = APIClient.get("/auth/user", headers={"Authorization": test_user["token"]})
        assert response.status_code == 200
        assert response.json()["user"]["email"] == test_user["email"]

    def test_create_existing_user(self, test_user):
        response = APIClient.post(REGISTER_ENDPOINT, test_user)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_missing_field(self, field):
        user = generate_user()
        del user[field]
        response = APIClient.post(REGISTER_ENDPOINT, user)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"

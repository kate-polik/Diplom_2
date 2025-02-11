import pytest
from utils.api_client import APIClient
from tests.constants import ORDERS_ENDPOINT


class TestOrders:

    def test_create_order_authorized(self, test_user):
        headers = {"Authorization": test_user["token"]}
        data = {"ingredients": ["60d3b41abdacab0026a733c6", "60d3b41abdacab0026a733c7"]}
        response = APIClient.post(ORDERS_ENDPOINT, data, headers=headers)
        assert response.status_code == 200
        assert "order" in response.json()

    def test_create_order_unauthorized(self):
        data = {"ingredients": ["60d3b41abdacab0026a733c6"]}
        response = APIClient.post(ORDERS_ENDPOINT, data)
        assert response.status_code == 401

    def test_create_order_no_ingredients(self, test_user):
        headers = {"Authorization": test_user["token"]}
        data = {"ingredients": []}
        response = APIClient.post(ORDERS_ENDPOINT, data, headers=headers)
        assert response.status_code == 400

    def test_create_order_invalid_ingredients(self, test_user):
        headers = {"Authorization": test_user["token"]}
        data = {"ingredients": ["invalid_id"]}
        response = APIClient.post(ORDERS_ENDPOINT, data, headers=headers)
        assert response.status_code == 400

    def test_get_orders_authorized(self, test_user):
        headers = {"Authorization": test_user["token"]}
        response = APIClient.get(ORDERS_ENDPOINT, headers=headers)
        assert response.status_code == 200
        assert "orders" in response.json()

    def test_get_orders_unauthorized(self):
        response = APIClient.get(ORDERS_ENDPOINT)
        assert response.status_code == 401

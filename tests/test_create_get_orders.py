import pytest
import allure
from utils.api_client import APIClient
from constants import APIEndpoints, TestData


@allure.epic("Заказы")
@allure.feature("Создание и получение заказов")
class TestGetUserOrdersEndpoint:
    """Тесты на создание и получение заказов"""

    def send_order_request(self, ingredients, headers=None):
        """Вспомогательный метод для отправки POST-запроса на создание заказа"""
        return APIClient.post(APIEndpoints.ORDERS, {"ingredients": ingredients}, headers=headers)

    def check_order_response(self, response, expected_status, expected_message=None):
        """Вспомогательный метод для проверки ответа API"""
        assert response.status_code == expected_status, f"Ожидался статус {expected_status}, но получен {response.status_code}"

        if expected_message:
            assert response.json() == expected_message, f"Ожидался ответ {expected_message}, но получен {response.json()}"
        elif expected_status == 200:
            response_json = response.json()
            assert response_json.get("success") is True, f"Ожидался success=True, но получен {response_json}"
            assert "name" in response_json, "В ответе отсутствует поле 'name'"
            assert "order" in response_json and "number" in response_json["order"], "В ответе отсутствует 'order' или 'number'"

    @allure.story("Создание заказов")
    @allure.title("Создание заказа с разными параметрами (авторизация, ингредиенты)")
    @pytest.mark.parametrize("auth, ingredients, expected_status, expected_message", TestData.ORDER_CASES)
    def test_create_order(self, test_user, auth, ingredients, expected_status, expected_message):
        """
        Тестирование создания заказа:
        - С авторизацией / без авторизации
        - С валидными / пустыми / невалидными ингредиентами
        """
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"} if auth else None
        response = self.send_order_request(ingredients, headers)

        with allure.step("Проверка ответа сервера"):
            if expected_status == 500:
                assert response.status_code == 500, f"Ожидался статус 500, но получен {response.status_code}"
                assert "Internal Server Error" in response.text, "Ожидалось сообщение 'Internal Server Error'"
            else:
                self.check_order_response(response, expected_status, expected_message)

    @allure.story("Получение списка заказов пользователя")
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, test_user):
        """
        Тест: Получение списка заказов авторизованного пользователя
        1. Создаем заказ
        2. Получаем заказы и проверяем данные
        """
        headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}

        with allure.step("Создание нового заказа"):
            order_response = APIClient.post(APIEndpoints.ORDERS, TestData.ORDER_PAYLOAD, headers=headers)
            assert order_response.status_code == 200, f"Ошибка при создании заказа: {order_response.status_code}"
            order_json = order_response.json()

            assert order_json["success"] is True, "Ожидался success=True, но получен False"
            assert "order" in order_json, "Ответ не содержит данных о заказе"
            created_order = order_json["order"]

        with allure.step("Проверка соответствия ингредиентов"):
            created_ingredients = [ingredient["_id"] for ingredient in created_order["ingredients"]]
            assert created_ingredients == TestData.ORDER_PAYLOAD["ingredients"], "Список ингредиентов не совпадает"

        with allure.step("Проверка владельца заказа"):
            assert created_order["owner"]["name"] == test_user["name"], "Имя владельца заказа не совпадает"
            assert created_order["owner"]["email"] == test_user["email"], "Email владельца заказа не совпадает"

        with allure.step("Проверка статуса и имени заказа"):
            assert created_order["status"] == "done", "Статус заказа должен быть 'done'"
            assert created_order["name"], "Имя заказа отсутствует в ответе"

        with allure.step("Получение списка заказов пользователя"):
            get_orders_response = APIClient.get(APIEndpoints.ORDERS, headers=headers)
            assert get_orders_response.status_code == 200, f"Ошибка при получении заказов: {get_orders_response.status_code}"

            orders_json = get_orders_response.json()
            assert orders_json["success"] is True, "Ожидался success=True, но получен False"
            assert "orders" in orders_json, "Ответ не содержит списка заказов"

            user_orders = orders_json["orders"]
            assert any(order["name"] == created_order["name"] for order in user_orders), "Созданный заказ отсутствует в списке заказов пользователя"

    @allure.story("Получение списка заказов без авторизации")
    @allure.title("Попытка получить заказы без авторизации")
    def test_get_orders_without_auth(self):
        """
        Тест: Попытка получения заказов без авторизации
        Ожидаемый результат:
        - Код ответа 401
        - Сообщение "You should be authorised"
        """

        with allure.step("Отправка GET-запроса без токена"):
            response = APIClient.get(APIEndpoints.ORDERS)

        with allure.step("Проверка ответа сервера"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"

            expected_response = {"success": False, "message": "You should be authorised"}
            assert response.json() == expected_response, f"Ожидался ответ {expected_response}, но получен {response.json()}"

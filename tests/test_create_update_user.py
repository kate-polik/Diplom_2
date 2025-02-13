import allure
import pytest
from utils.api_client import APIClient
from constants import APIEndpoints, TestUserDataUpdate, ErrorMessages
from utils.data_generator import generate_user


@allure.epic("Пользователи")
@allure.feature("Работа с профилем")
class TestUserEndpoint:
    """Тесты эндпоинта пользователя"""

    @allure.story("Получение данных пользователя")
    @allure.title("Проверка существования созданного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user(self, test_user):
        """Проверяет, что созданный пользователь существует"""
        with allure.step("Отправка запроса на получение данных пользователя"):
            response = APIClient.get(APIEndpoints.USER, headers={"Authorization": test_user["token"]})

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

        with allure.step("Проверка, что email пользователя соответствует ожидаемому"):
            assert response.json()["user"]["email"] == test_user["email"], "Email пользователя не совпадает"

    @pytest.mark.parametrize("update_data, field, expected_status, expected_response", TestUserDataUpdate.UPDATE_CASES)
    @allure.story("Обновление данных пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user_data(self, test_user, update_data, field, expected_status, expected_response):
        """
        Тест на изменение данных пользователя:
        - С авторизацией (ожидаем статус 200)
        - Без авторизации (ожидаем статус 401 и сообщение об ошибке)
        """
        auth_status = "с авторизацией" if expected_status == 200 else "без авторизации"
        allure.dynamic.title(f"Тест обновления поля {field} ({auth_status})")

        headers = {"Authorization": test_user["token"],
                   "Content-Type": "application/json"} if expected_status == 200 else {}

        with allure.step(f"Отправка запроса на обновление {field}"):
            response = APIClient.patch(APIEndpoints.USER, data=update_data, headers=headers)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == expected_status, f"Ошибка при обновлении {field}, статус {response.status_code}"

        if expected_response:
            with allure.step("Проверка сообщения об ошибке"):
                assert response.json() == expected_response, f"Ожидался ответ {expected_response}, но получен {response.json()}"
        elif field in response.json().get("user", {}):
            with allure.step(f"Проверка, что {field} обновился корректно"):
                assert response.json()["user"][field] == update_data[field], f"{field} не обновился"


@allure.epic("Пользователи")
@allure.feature("Регистрация")
class TestUserRegisterEndpoint:
    """Тесты регистрации пользователя"""

    @allure.story("Регистрация существующего пользователя")
    @allure.title("Попытка зарегистрировать уже существующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user(self, test_user):
        """Проверяет, что нельзя зарегистрировать уже существующего пользователя"""
        with allure.step("Отправка запроса на регистрацию уже существующего пользователя"):
            response = APIClient.post(APIEndpoints.REGISTER, test_user)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["message"] == ErrorMessages.USER_EXISTS, "Сообщение об ошибке не совпадает"

    @pytest.mark.parametrize("field", TestUserDataUpdate.REQUIRED_FIELDS)
    @allure.story("Регистрация пользователя без обязательного поля")
    @allure.title("Регистрация без поля {field}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_missing_field(self, field):
        """Проверяет, что регистрация невозможна без одного из обязательных полей"""
        user = generate_user()
        del user[field]

        with allure.step(f"Отправка запроса на регистрацию без поля {field}"):
            response = APIClient.post(APIEndpoints.REGISTER, user)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, но получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["message"] == ErrorMessages.REQUIRED_FIELDS, "Сообщение об ошибке не совпадает"

import pytest
from utils.api_client import APIClient
from utils.data_generator import generate_user
from tests.constants import REGISTER_ENDPOINT
from tests.constants import USER_ENDPOINT
import requests


# @pytest.fixture
# def test_user():
#     """Создаёт тестового пользователя перед тестом и удаляет его после теста"""
#     user = generate_user()
#     response = APIClient.post(REGISTER_ENDPOINT, user)
#     assert response.status_code == 200, "Ошибка создания тестового пользователя"
#
#     token = response.json().get("accessToken")
#     assert token, "Не получен accessToken при регистрации"
#
#     user["token"] = token
#
#     yield user  # Передаём данные пользователя в тест
#
#     # Удаляем пользователя, если токен есть
#     if "token" in user:
#         delete_response = APIClient.delete("/auth/user", headers={"Authorization": user["token"]})
#         assert delete_response.status_code == 202, "Ошибка удаления тестового пользователя"


# import pytest
# from utils.data_generator import generate_user
# from utils.api_client import APIClient  # Оставляем APIClient для совместимости
#
# REGISTER_ENDPOINT = "https://stellarburgers.nomoreparties.site/api/auth/register"
# USER_ENDPOINT = "https://stellarburgers.nomoreparties.site/api/auth/user"

# @pytest.fixture
# def test_user():
#     """Создаёт тестового пользователя перед тестом и удаляет его после теста"""
#     user = generate_user()
#     response = APIClient.post(REGISTER_ENDPOINT, user)
#     assert response.status_code == 200, "Ошибка создания тестового пользователя"
#
#     token = response.json().get("accessToken")
#     assert token, "Не получен accessToken при регистрации"
#
#     # Сохраняем токен, email и name, чтобы тесты могли их использовать
#     user["token"] = token
#     user["email"] = response.json()["user"]["email"]
#     user["name"] = response.json()["user"]["name"]
#
#     yield user  # Передаём данные пользователя в тест
#
#     # Удаляем пользователя, если токен есть
#     headers = {"Authorization": user["token"]}
#     delete_response = APIClient.delete(USER_ENDPOINT, headers=headers)
#     assert delete_response.status_code == 202, "Ошибка удаления тестового пользователя"

import pytest
from utils.api_client import APIClient
from tests.constants import REGISTER_ENDPOINT, USER_ENDPOINT
from utils.data_generator import generate_user


@pytest.fixture
def test_user():
    """Создаёт тестового пользователя перед тестом и удаляет его после теста"""
    user = generate_user()

    response = APIClient.post(REGISTER_ENDPOINT, user)
    assert response.status_code == 200, f"Ошибка создания тестового пользователя: {response.text}"

    token = response.json().get("accessToken")
    assert token, "Не получен accessToken при регистрации"

    # Добавляем в user токен, email, name и password
    user.update({
        "token": token,
        "email": response.json()["user"]["email"],
        "name": response.json()["user"]["name"],
        "password": user["password"]  # добавляем пароль для логина
    })

    yield user  # Передаём данные пользователя в тест

    # Удаляем пользователя, если токен есть
    headers = {"Authorization": user["token"]}
    try:
        delete_response = APIClient.delete(USER_ENDPOINT, headers=headers)
        assert delete_response.status_code == 202, f"Ошибка удаления тестового пользователя: {delete_response.text}"
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")


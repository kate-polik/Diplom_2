import pytest
from utils.data_generator import generate_user
import requests

REGISTER_ENDPOINT = "https://stellarburgers.nomoreparties.site/api/auth/register"
LOGIN_ENDPOINT = "https://stellarburgers.nomoreparties.site/api/auth/login"
USER_ENDPOINT = "https://stellarburgers.nomoreparties.site/api/auth/user"


# @pytest.fixture
# def test_user():
#     """Создаёт тестового пользователя перед тестом и удаляет его после теста"""
#     user = generate_user()
#     response = requests.post(REGISTER_ENDPOINT, json=user)
#     assert response.status_code == 200, "Ошибка создания тестового пользователя"
#
#     token = response.json().get("accessToken")
#     assert token, "Не получен accessToken при регистрации"
#
#     user["token"] = token
#     user["email"] = response.json()["user"]["email"]
#     user["name"] = response.json()["user"]["name"]
#
#     yield user  # Передаём данные пользователя в тест
#
#     # Удаляем пользователя, если токен есть
#     headers = {"Authorization": user["token"]}
#     delete_response = requests.delete(USER_ENDPOINT, headers=headers)
#     assert delete_response.status_code == 202, "Ошибка удаления тестового пользователя"


def test_update_user_data(test_user):
    """Тест: Изменение данных пользователя (email, имя, пароль) с авторизацией"""
    headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}

    # **1. Изменение email**
    new_email = "updated_test@example.com"
    response = requests.patch(USER_ENDPOINT, json={"email": new_email}, headers=headers)
    assert response.status_code == 200, "Ошибка при обновлении email"
    assert response.json()["user"]["email"] == new_email, "Email не обновился"

    # **2. Изменение имени**
    new_name = "UpdatedUser"
    response = requests.patch(USER_ENDPOINT, json={"name": new_name}, headers=headers)
    assert response.status_code == 200, "Ошибка при обновлении имени"
    assert response.json()["user"]["name"] == new_name, "Имя не обновилось"

    # **3. Изменение пароля**
    new_password = "NewPass123"
    response = requests.patch(USER_ENDPOINT, json={"password": new_password}, headers=headers)
    assert response.status_code == 200, "Ошибка при обновлении пароля"

    # **Проверяем, что email и имя остались такими же**
    assert response.json()["user"]["email"] == new_email, "Email изменился после смены пароля"
    assert response.json()["user"]["name"] == new_name, "Имя изменилось после смены пароля"

    print("✅ Все изменения данных прошли успешно")

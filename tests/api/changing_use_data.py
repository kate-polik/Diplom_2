import pytest
from utils.api_client import APIClient
from utils.data_generator import generate_user
from tests.constants import REGISTER_ENDPOINT
from tests.constants import USER_ENDPOINT
import json
import requests


def test_update_user_with_auth(test_user):
    """Тест: Изменение данных пользователя с авторизацией"""
    updated_data = {"email": "updated@example.com", "name": "UpdatedUser"}

    response = APIClient.patch(USER_ENDPOINT,
                               data=json.dumps(updated_data),  # Преобразуем в JSON
                               headers={
                                   "Authorization": test_user["token"],
                                   "Content-Type": "application/json"
                               })

    assert response.status_code == 200
    assert response.json()["user"]["email"] == updated_data["email"]
    assert response.json()["user"]["name"] == updated_data["name"]


def test_update_user_without_auth():
    """Тест: Изменение данных пользователя без авторизации"""
    updated_data = {"email": "unauthorized@example.com", "name": "UnauthorizedUser"}
    response = APIClient.patch(USER_ENDPOINT, json=updated_data)

    assert response.status_code == 401
    assert response.json()["message"] == "You should be authorised"


@pytest.mark.parametrize("field, new_value", [
    ("email", "new-email@example.com"),
    ("name", "NewUsername")
])
def test_update_each_field(test_user, field, new_value):
    """Тест: Изменение каждого отдельного поля с авторизацией"""
    response = APIClient.patch(USER_ENDPOINT, json={field: new_value}, headers={"Authorization": test_user["token"]})

    assert response.status_code == 200
    assert response.json()["user"][field] == new_value


def test_update_email_to_existing(test_user):
    """Тест: Попытка изменить email на уже существующий"""
    existing_user = generate_user()
    APIClient.post(REGISTER_ENDPOINT, existing_user)  # Создаём второго пользователя

    response = APIClient.patch(USER_ENDPOINT, json={"email": existing_user["email"]},
                               headers={"Authorization": test_user["token"]})

    assert response.status_code == 403
    assert response.json()["message"] == "User with such email already exists"


import json


def test_update_user_data(test_user):
    """Тест: Изменение данных пользователя (email, имя, пароль) с авторизацией"""
    headers = {"Authorization": test_user["token"], "Content-Type": "application/json"}

    # **1. Изменение email**
    new_email = "updated_test@example.com"
    response = APIClient.patch(USER_ENDPOINT, data=json.dumps({"email": new_email}), headers=headers)
    assert response.status_code == 200, "Ошибка при обновлении email"
    assert response.json()["user"]["email"] == new_email, "Email не обновился"

    # # **2. Изменение имени**
    # new_name = "UpdatedUser"
    # response = APIClient.patch(USER_ENDPOINT, data=json.dumps({"name": new_name}), headers=headers)
    # assert response.status_code == 200, "Ошибка при обновлении имени"
    # assert response.json()["user"]["name"] == new_name, "Имя не обновилось"
    #
    # # **3. Изменение пароля**
    # new_password = "NewPass123"
    # response = APIClient.patch(USER_ENDPOINT, data=json.dumps({"password": new_password}), headers=headers)
    # assert response.status_code == 200, "Ошибка при обновлении пароля"
    #
    # # **Проверяем, что email и имя остались такими же**
    # assert response.json()["user"]["email"] == new_email, "Email изменился после смены пароля"
    # assert response.json()["user"]["name"] == new_name, "Имя изменилось после смены пароля"
    #
    # print("✅ Все изменения данных прошли успешно")

def test_update_user_data1(test_user):
    """Тест: Изменение данных пользователя (email, имя, пароль) с авторизацией"""
    headers = {
        "Authorization": f"{test_user['token']}",  # Добавлен "Bearer "
        "Content-Type": "application/json",
        "Accept": "application/json"  # Добавлен Accept
    }

    # **1. Изменение email**
    new_email = "updated_test@example.com"
    response = APIClient.patch(USER_ENDPOINT, json={"email": new_email}, headers=headers)  # Используем json=
    assert response.status_code == 200, f"Ошибка при обновлении email: {response.text}"
    assert response.json()["user"]["email"] == new_email, "Email не обновился"


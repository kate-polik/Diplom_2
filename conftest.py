import pytest
from utils.api_client import APIClient
from constants import APIEndpoints
from utils.data_generator import generate_user
import os
import shutil


@pytest.fixture
def test_user():
    """Создаёт тестового пользователя перед тестом и удаляет его после теста"""
    user = generate_user()

    response = APIClient.post(APIEndpoints.REGISTER, user)

    token = response.json().get("accessToken")

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
    APIClient.delete(APIEndpoints.USER, headers=headers)


# Хук для очистки allure_results
def pytest_sessionstart(session):
    """Очистка папки allure_results перед запуском тестов."""
    results_dir = "allure_results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)

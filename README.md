# Дипломный проект. Задание 2: Тесты API Stellar Burgers

## Описание проекта
Проект содержит автотесты для API сервиса **Stellar Burgers**.  
В тестах проверяются различные сценарии работы API, включая создание пользователей, авторизацию, обновление данных и работу с заказами.  

## Структура проекта  
Проект организован следующим образом:  

```
Diplom_2/
├── allure_results/              # Папка для хранения результатов тестов Allure
├── tests/
│   ├── test_auth.py             # Тесты авторизации
│   ├── test_create_get_orders.py # Тесты создания и получения заказов
│   ├── test_create_update_user.py # Тесты создания и обновления пользователя
├── utils/
│   ├── __init__.py              # Инициализация модуля
│   ├── api_client.py            # Клиент для работы с API
│   ├── data_generator.py        # Генератор тестовых данных
├── .gitignore                   # Исключение ненужных файлов из Git
├── conftest.py                  # Фикстуры и настройки для тестов
├── constants.py                 # Константы (API-эндпоинты, тестовые данные и сообщения об ошибках)
├── pytest.ini                   # Конфигурация для pytest
├── README.md                    # Описание проекта                   
├── requirements.txt             # Список зависимостей проекта

```

## Описание тестов  

### **1. Тесты создания и обновления пользователя** (`test_create_update_user.py`)  
- **Создание уникального пользователя** — `test_create_unique_user`
- **Создание уже зарегистрированного пользователя** — `test_create_existing_user`
- **Создание пользователя без обязательного поля** — `test_create_user_missing_field`
- **Обновление данных пользователя:**
  - С авторизацией + Проверка успешного изменения данных  — `test_update_email_with_auth`, `test_update_name_with_auth`, `test_update_password_with_auth`
  - Без авторизации + Проверка ошибки при отсутствии авторизации — `test_update_email_without_auth`, `test_update_name_without_auth`, `test_update_password_without_auth`

### **2. Тесты авторизации** (`test_auth.py`)  
- **Авторизация с существующими учетными данными** — `test_login_existing_user`
- **Авторизация с неверными данными** — `test_login_invalid_credentials`

### **3. Тесты создания и получения заказов** (`test_create_get_orders.py`)  
- **Создание заказа**:  
  - С авторизацией + С ингредиентами — `test_create_order_with_auth_valid_ingredients`
  - С авторизацией + Без ингредиентов — `test_create_order_with_auth_empty_ingredients` 
  - С авторизацией + С неверными идентификаторами ингредиентов — `test_create_order_with_auth_invalid_ingredients`
  - Без авторизации + С ингредиентами — `test_create_order_without_auth_valid_ingredients` 
  - Без авторизации + Без ингредиентов — `test_create_order_without_auth_empty_ingredients`
  - Без авторизации + С неверными идентификаторами ингредиентов — `test_create_order_without_auth_invalid_ingredients`
- **Получение заказов пользователя**:  
  - Авторизованный пользователь (`test_get_orders_with_auth`)
  - Неавторизованный пользователь (`test_get_orders_without_auth`)

## Технические требования  
- **Корректные названия** для пакетов, файлов, классов, методов и переменных  
- **Отдельные классы** для тестирования каждого эндпоинта  
- **Все тесты успешно проходят**  
- **Полное покрытие тестами всех требований задания**  
- **Проверка и кода ответа, и тела запроса**  
- **Независимые тесты** (данные создаются перед тестом и удаляются после выполнения)  
- **Генерация Allure-отчёта**  

## Запуск тестов  
1. Установите зависимости:  
   ```sh
   pip3 install -r requirements.txt
    ```
2. Запустите тесты:  
   ```sh
    pytest tests --alluredir=allure_results
    ```
3. Сгенерируйте отчёт Allure::  
   ```sh
   allure serve allure_results  
    ```

class APIEndpoints:
    """API эндпоинты"""
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"
    REGISTER = "/auth/register"
    USER = "/auth/user"
    ORDERS = "/orders"
    LOGIN = "/auth/login"


class Ingredients:
    """ID ингредиентов"""
    VALID = ["61c0c5a71d1f82001bdaaa7a", "61c0c5a71d1f82001bdaaa6f"]
    EMPTY = []
    INVALID = ["6c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f001bdaaa6f"]
    FULL = [
        "61c0c5a71d1f82001bdaaa7a",
        "61c0c5a71d1f82001bdaaa6f",
        "61c0c5a71d1f82001bdaaa77",
        "61c0c5a71d1f82001bdaaa79"
    ]


class ErrorMessages:
    """Ожидаемые сообщения об ошибках"""
    NO_INGREDIENTS = {"success": False, "message": "Ingredient ids must be provided"}
    SERVER_ERROR = "Internal Server Error"
    INVALID_CREDENTIALS = {"success": False, "message": "email or password are incorrect"}
    USER_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"


class TestData:
    """Тестовые данные"""
    ORDER_CASES = [
        (True, Ingredients.VALID, 200, None),
        (False, Ingredients.VALID, 200, None),
        (True, Ingredients.EMPTY, 400, ErrorMessages.NO_INGREDIENTS),
        (False, Ingredients.EMPTY, 400, ErrorMessages.NO_INGREDIENTS),
        (True, Ingredients.INVALID, 500, ErrorMessages.SERVER_ERROR),
        (False, Ingredients.INVALID, 500, ErrorMessages.SERVER_ERROR),
    ]

    ORDER_PAYLOAD = {"ingredients": Ingredients.FULL}


class TestUserData:
    """Тестовые данные для входа"""
    INVALID_CREDENTIALS = {"email": "wrong@example.com", "password": "wrongpass"}


class TestUserDataUpdate:
    """Тестовые данные пользователя"""
    UPDATE_CASES = [
        ({"email": "updated_test@example.com"}, "email", 200, None),
        ({"name": "UpdatedUser"}, "name", 200, None),
        ({"password": "NewPass123"}, "password", 200, None),
        (
        {"email": "unauthorized@example.com"}, "email", 401, {"success": False, "message": "You should be authorised"}),
        ({"name": "UnauthorizedUser"}, "name", 401, {"success": False, "message": "You should be authorised"}),
        ({"password": "UnauthorizedPass"}, "password", 401, {"success": False, "message": "You should be authorised"}),
    ]
    REQUIRED_FIELDS = ["email", "password", "name"]

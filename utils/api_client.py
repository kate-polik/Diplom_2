import requests


class APIClient:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"

    @staticmethod
    def post(endpoint, data, headers=None):
        return requests.post(f"{APIClient.BASE_URL}{endpoint}", json=data, headers=headers)

    @staticmethod
    def get(endpoint, headers=None):
        return requests.get(f"{APIClient.BASE_URL}{endpoint}", headers=headers)

    @staticmethod
    def patch(endpoint, data, headers=None):
        return requests.patch(f"{APIClient.BASE_URL}{endpoint}", json=data, headers=headers)

    @staticmethod
    def delete(endpoint, headers=None):
        return requests.delete(f"{APIClient.BASE_URL}{endpoint}", headers=headers)

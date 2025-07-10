import pytest
from fastapi.testclient import TestClient


class TestLogin:
    def test_login_returns_200(self, register, client: TestClient):
        resp = client.post(
            "/api/auth/login",
            data={"username": "example", "password": "example123"},
        )

        assert resp.status_code == 200

    @pytest.mark.parametrize(
        "username,password", [("false", "example123"), ("example", "false")]
    )
    def test_login_with_invalid_data_returns_400(
        self, register, username: str, password: str, client: TestClient
    ):
        resp = client.post(
            "/api/auth/login",
            data={"username": username, "password": password},
        )

        assert resp.status_code == 400

    @pytest.mark.parametrize(
        "data",
        [
            ({"username": None, "password": "example123"}),
            ({"username": "example", "password": None}),
        ],
    )
    def test_login_with_no_data_returns_400(
        self, register, data: dict, client: TestClient
    ):
        resp = client.post(
            "/api/auth/login",
            data=data,
        )

        assert resp.status_code == 400

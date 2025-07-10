import pytest
from fastapi.testclient import TestClient


class TestLogin:
    def test_login_returns_200(self, register: None, client: TestClient):
        resp = client.post(
            "/api/login",
            data={"username": "example", "password": "example123"},
        )

        assert resp.status_code == 200

    @pytest.mark.parametrize(
        "username,password", [("false", "example123"), ("example", "false")]
    )
    def test_login_with_invalid_data_returns_400(
        self, register: None, username: str, password: str, client: TestClient
    ):
        resp = client.post(
            "/api/login",
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
        self, register: None, data: dict, client: TestClient
    ):
        resp = client.post(
            "/api/login",
            data=data,
        )

        assert resp.status_code == 400


class TestRegister:
    @pytest.mark.parametrize(
        "body",
        (
            {
                "name": "example",
                "password": "example123",
                "email": "example@gmail.com",
            },
            {
                "name": "example",
                "password": "example123",
            },
        ),
    )
    def test_register_returns_201(self, body: dict[str, str], client: TestClient):
        resp = client.post("/api/register", json=body)

        assert resp.status_code == 201

    @pytest.mark.parametrize(
        "body",
        ({"name": "example", "email": "example@gmail.com"}, {"password": "example123"}),
    )
    def test_register_with_wrong_body_returns_422(self, body: dict[str, str], client: TestClient):
        resp = client.post(
            "/api/register",
            json=body,
        )

        assert resp.status_code == 422

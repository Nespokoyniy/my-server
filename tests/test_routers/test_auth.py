import pytest
from fastapi.testclient import TestClient


class TestLogin:
    def test_post_login_returns_200(self, register: None, client: TestClient):
        resp = client.post(
            "/api/login",
            data={"username": "example", "password": "example123"},
        )
        assert resp.status_code == 200

    @pytest.mark.parametrize(
        "username,password", [("false", "example123"), ("example", "false")]
    )
    def test_post_login_with_invalid_credentials_returns_400(
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
    def test_post_login_with_missing_fields_returns_400(
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
    def test_post_register_returns_201(self, body: dict[str, str], client: TestClient):
        resp = client.post("/api/register", json=body)
        assert resp.status_code == 201

    @pytest.mark.parametrize(
        "body",
        ({"name": "example", "email": "example@gmail.com"}, {"password": "example123"}),
    )
    def test_post_register_with_invalid_body_returns_422(
        self, body: dict[str, str], client: TestClient
    ):
        resp = client.post("/api/register", json=body)
        assert resp.status_code == 422

# class TestLogout:
#     def test_logout_returns_204(client: TestClient, token):
#         resp = client.delete()
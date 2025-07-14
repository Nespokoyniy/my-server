from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import select
import pytest
from typing import Any
from backend.app.database import models
from backend.app.utils.dependencies import get_current_user


class TestGetProfile:
    def test_get_profile_returns_200(self, client: TestClient, token: dict[str, str]):
        resp = client.get("/api/profile", headers=token)
        assert resp.status_code == 200

    def test_get_profile_auth_returns_401(self, client: TestClient):
        resp = client.get("/api/profile")
        assert resp.status_code == 401


class TestDeleteProfile:
    def test_delete_profile_returns_204(
        self, client: TestClient, token: dict[str, str], test_db: Session
    ):
        user_id = get_current_user(token["Authorization"].split()[1], test_db)
        assert (
            test_db.execute(
                select(models.User).where(models.User.id == user_id)
            ).scalar_one_or_none()
            is not None
        )

        resp = client.delete("/api/profile", headers=token)
        assert resp.status_code == 204

        assert (
            test_db.execute(
                select(models.User).where(models.User.id == user_id)
            ).scalar_one_or_none()
            is None
        )

        assert (
            test_db.execute(
                select(models.RefreshToken).where(models.RefreshToken.owner == user_id)
            ).scalar_one_or_none()
            is None
        )

    def test_delete_profile_returns_401(self, client: TestClient):
        resp = client.delete("/api/profile")
        assert resp.status_code == 401


class TestUpdateProfile:
    @pytest.mark.parametrize(
        "body",
        (
            {
                "name": "new example",
                "password": "new example123",
                "email": "newexample@gmail.com",
            },
            {"name": "new example123", "password": "new example123"},
            {
                "name": "example",
                "password": "new example123",
                "email": "newexample@gmail.com",
            },
        ),
    )
    def test_update_profile_returns_200(
        self, body: dict[str, str], client: TestClient, token: dict[str, str]
    ):
        resp = client.put("/api/profile", json=body, headers=token)
        assert resp.status_code == 200

    def test_update_profile_auth_returns_401(self, client: TestClient):
        resp = client.put(
            "/api/profile", json={"name": "example", "password": "example123"}
        )
        assert resp.status_code == 401

    @pytest.mark.parametrize(
        "body",
        (
            {"name": "new example"},
            {"password": "new example123"},
            {"email": "newexample@gmail.com"},
        ),
    )
    def test_update_profile_with_invalid_data_returns_422(
        self, body: dict[Any, Any], client: TestClient, token: dict[str, str]
    ):
        resp = client.put("/api/profile", json=body, headers=token)
        assert resp.status_code == 422

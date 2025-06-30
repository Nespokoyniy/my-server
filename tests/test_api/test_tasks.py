import pytest
from fastapi.testclient import TestClient
from fastapi import Depends

class TestGetTasks():
    
    @pytest.mark.positive
    def test_get_tasks_returns_200(self, token, client: TestClient):
        tasks = client.get("http://localhost:8000/api/tasks", headers=token)
        assert tasks.status_code == 200
    
    @pytest.mark.negative
    def test_auth_returns_401(self, client: TestClient):
        resp = client.get("http://localhost:8000/api/tasks")
        assert resp.status_code == 401
import fastapi.testclient
import pytest
import fastapi

class TestGetTasks():
    
    @pytest.mark.positive
    def test_get_tasks_gets_returns_200(self, client: fastapi.testclient.TestClient):
        resp = client.post("/login", content={})
    
    @pytest.mark.negative
    def test_get_tasks_auth_returns_401(self, client):
        resp = client.get("/api/tasks")
        assert resp.status_code == 401
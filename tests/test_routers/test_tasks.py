from fastapi.testclient import TestClient
import pytest

class TestGetTasks():
    
    def test_get_tasks_returns_200(self, token, client: TestClient):
        tasks = client.get("/api/tasks", headers=token)
        assert tasks.status_code == 200
        
    def test_get_tasks_auth_returns_401(self, client: TestClient):
        resp = client.get("/api/tasks")
        assert resp.status_code == 401
        
class CompleteUncompleteTask():
    
    def test_complete_uncomplete_task_returns_200(self, token, client: TestClient):
        client.post("/api/tasks", json={"name": "task", "description": "new task", "priority": 6})
        task = client.put("/api/tasks/1/")
        assert task.status_code == 200
        assert task.is_completed == True
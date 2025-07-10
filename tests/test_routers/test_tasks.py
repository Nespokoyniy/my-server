from fastapi.testclient import TestClient
import pytest


class TestGetTasks:
    def test_get_tasks_returns_200(self, token, create_tasks, client: TestClient):
        tasks = client.get("/api/tasks", headers=token)
        assert tasks.status_code == 200

    def test_get_tasks_auth_returns_401(self, create_tasks, client: TestClient):
        resp = client.get("/api/tasks")
        assert resp.status_code == 401


class TestCompleteUncompleteTask:
    def test_complete_uncomplete_task_returns_200(
        self, token, create_tasks, client: TestClient
    ):
        task = client.put("/api/tasks/1/status", headers=token)
        assert task.status_code == 200
        assert task.json()["is_completed"] == True
        task = client.put("/api/tasks/1/status", headers=token)
        assert task.status_code == 200
        assert task.json()["is_completed"] == False

    def test_complete_uncomplete_task_auth_returns_401(
        self, create_tasks, client: TestClient
    ):
        resp = client.put("/api/tasks/1/status")
        assert resp.status_code == 401

    def test_complete_uncomplete_task_returns_404(
        self, token, create_tasks, client: TestClient
    ):
        resp = client.put("/api/tasks/0/status", headers=token)
        assert resp.status_code == 404

    def test_complete_uncomplete_task_user_doesnt_own_returns_404(
        self, token, token_2, create_tasks, client: TestClient
    ):
        resp = client.put("/api/tasks/1/status", headers=token)
        resp_2 = client.put("/api/tasks/1/status", headers=token_2)
        assert resp.status_code != resp_2


class TestCreateTask:
    def test_create_task_returns_201(self, token, create_tasks, client: TestClient):
        resp = client.post(
            "/api/tasks",
            json={"name": "new task", "description": "new description", "priority": 8},
            headers=token,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "new task"
        assert data["user_task_id"] == 4

    @pytest.mark.parametrize(
        "body",
        ({"description": "new description", "priority": 5}),
    )
    def test_create_task_with_invalid_input_returns_422(
        self, body, token, client: TestClient
    ):
        resp = client.post(
            "/api/tasks",
            json=body,
            headers=token,
        )
        assert resp.status_code == 422

    def test_create_task_auth_returns_401(self, client: TestClient):
        resp = client.post(
            "/api/tasks",
            json={"description": "new description", "priority": 5},
        )
        assert resp.status_code == 401


class TestGetTask:
    def test_get_task_returns_200(self, create_tasks, client: TestClient, token):
        resp = client.get("/api/tasks/1", headers=token)
        assert resp.status_code == 200
        assert resp.json()["name"] == "task 1"

    def test_get_task_returns_401(self, create_tasks, client: TestClient):
        resp = client.get("/api/tasks/1")
        assert resp.status_code == 401

    def test_get_task_returns_404(self, create_tasks, client: TestClient, token):
        resp = client.get("/api/tasks/0", headers=token)
        assert resp.status_code == 404

    def test_get_task_user_doesnt_own_returns_404(
        self, token, token_2, create_tasks, client: TestClient
    ):
        resp = client.put("/api/tasks/1", headers=token)
        resp_2 = client.put("/api/tasks/1", headers=token_2)
        assert resp.status_code != resp_2

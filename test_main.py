from fastapi.testclient import TestClient
from main import app, tasks

client = TestClient(app)


def setup_function():
    """Reset the in-memory task list before each test."""
    tasks.clear()
    tasks.extend([
        {"id": 1, "title": "Learn FastAPI", "done": False},
        {"id": 2, "title": "Build a CRUD API", "done": False},
        {"id": 3, "title": "Publish project on GitHub", "done": False},
    ])


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Task API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_missing_task():
    response = client.get("/tasks/99")
    assert response.status_code == 404


def test_create_task():
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    assert response.json()["title"] == "Write tests"
    assert response.json()["done"] is False


def test_update_task():
    response = client.put(
        "/tasks/1",
        json={"title": "Updated task", "done": True}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated task"
    assert response.json()["done"] is True


def test_delete_task():
    response = client.delete("/tasks/2")
    assert response.status_code == 204
    assert client.get("/tasks/2").status_code == 404
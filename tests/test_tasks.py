# tests/test_tasks.py

import uuid
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    email = f"task-{uuid.uuid4().hex[:8]}@example.com"
    password = "taskpass"
    # Реєстрація
    client.post("/auth/register", json={"name": "Tasker", "email": email, "password": password})

    # Логін
    res = client.post("/auth/login", data = {"username": email, "password": password})

    assert res.status_code == status.HTTP_200_OK, res.text
    return res.json()["access_token"]

def test_tasks_crud_flow():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1) створюємо таск
    payload = {"title":"Write tests","description":"desc","status":"pending","priority":2}
    res = client.post("/tasks/", json=payload, headers=headers)
    assert res.status_code == status.HTTP_200_OK, res.text
    task = res.json()
    task_id = task["id"]

    # 2) читаємо список
    res = client.get("/tasks/", headers=headers)
    assert res.status_code == status.HTTP_200_OK
    assert any(t["id"] == task_id for t in res.json())

    # 3) оновлюємо таск
    res = client.put(f"/tasks/{task_id}", json={"status":"done","priority":5}, headers=headers)
    assert res.status_code == status.HTTP_200_OK
    upd = res.json()
    assert upd["status"] == "done"
    assert upd["priority"] == 5

    # 4) шукаємо
    res = client.get("/tasks/search", params={"q":"Write"}, headers=headers)
    assert res.status_code == status.HTTP_200_OK
    assert any(t["id"] == task_id for t in res.json())
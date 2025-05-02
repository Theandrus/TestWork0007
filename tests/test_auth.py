from fastapi.testclient import TestClient
import uuid
from fastapi import status
from app.main import app

client = TestClient(app)

def test_register_login_refresh():
    # 1) Реєстрація
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    password = "securepassword"
    res = client.post(
        "/auth/register",
        json={"name": "Tester", "email": email, "password": password}
    )
    assert res.status_code == status.HTTP_200_OK, res.text
    data = res.json()
    assert data["email"] == email
    assert "id" in data

    # 2) Логін
    res = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    assert res.status_code == status.HTTP_200_OK, res.text
    tokens = res.json()
    assert "access_token" in tokens
    access = tokens["access_token"]
    assert "refresh_token" in tokens
    refresh = tokens["refresh_token"]

    # 3) Оновлення токена
    res = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh}
    )
    assert res.status_code == status.HTTP_200_OK, res.text
    new_tokens = res.json()
    assert "access_token" in new_tokens

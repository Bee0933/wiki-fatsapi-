from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# test new user
def test_create_user():
    response = client.post(
        "/auth/sign-in",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "pass",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "status_code": 400,
        "detail": "user email already exists",
        "headers": None,
    }

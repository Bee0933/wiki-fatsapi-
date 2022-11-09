from fastapi.testclient import TestClient
from api import app
import secrets

# client instance
client = TestClient(app)


# test signin route
def test_sigin_route():
    mail = f"{secrets.token_hex(16)}@mail.com"
    uname = str(secrets.token_hex(8))
    response = client.post(
        "/auth/sign-in",
        json={
            "username": uname,
            "email": mail,
            "password": "pass",
        },
    )
    assert response.status_code == 201
    data = response.json()
    print("here" * 10)
    print(data)
    assert data["email"] == mail
    assert "id" in data


# test login
def test_login_route():
    response = client.post(
        "/auth/log-in", json={"email": "testuser0@mail.com", "password": "pass"}
    )
    print("here" * 20)
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["access token"] != " " and data["refresh token"] != " "


# test bad login
def test_bad_login():
    response = client.post(
        "/auth/log-in",
        json={
            "email": "testuser0fault@mail.com",
            "password": "pass",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid email or password"


# test refresh route
def test_refresh():
    response = client.post(
        "/auth/log-in", json={"email": "testuser0@mail.com", "password": "pass"}
    )
    assert response.status_code == 201
    data = response.json()
    refresh_token = data["refresh token"]

    response2 = client.get(
        "/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["access token"] != " "


# test single user route
def single_user():
    usrid = 8
    response = client.get(f"/{usrid}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usrid


# te0st search-titles route
def test_search_titles():
    response = client.post(
        "/auth/log-in", json={"email": "testuser0@mail.com", "password": "pass"}
    )
    assert response.status_code == 201
    data = response.json()
    access_token = data["access token"]

    response2 = client.post(
        "/wiki/search-titles",
        json={"key": "samsung"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response2.status_code == 201
    data2 = response2.json()
    assert data2["message"] != []


def test_search_pages():
    response = client.post(
        "/auth/log-in", json={"email": "testuser0@mail.com", "password": "pass"}
    )
    assert response.status_code == 201
    data = response.json()
    access_token = data["access token"]

    response2 = client.post(
        "/wiki/search-pages",
        json={"title": "Samsung"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response2.status_code == 201
    data2 = response2.json()
    assert len(data2["content"]) > 5

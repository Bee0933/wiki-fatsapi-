from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api import app, get_db
from db import Base
import secrets


DB_URL = "sqlite:///db/test.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create db
Base.metadata.create_all(bind=engine)

# override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# client instance
client = TestClient(app)

# test single user route
def test_database():
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
    assert data["email"] == mail
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/auth/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == mail
    assert data["id"] == user_id

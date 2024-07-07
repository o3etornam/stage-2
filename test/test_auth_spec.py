from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import get_db
from app.models import Base
from app.oauth2 import get_current_user
from app import schema

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    return schema.User(
        userId="1",
        firstName="John",
        lastName="Doe",
        email="john.doe@example.com",
        phone="1234567890",
    )


client = TestClient(app=app)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_create_user():
    response = client.post(
        "/auth/register",
        headers={"X-Token": "coneofsilence"},
        json={
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "password": "securepassword",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "status": "success",
        "message": "Registration Successful",
        "data": {
            "accessToken": response.json()["data"]["accessToken"],
            "user": {
                "userId": response.json()["data"]["user"]["userId"],
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
            },
        },
    }


def test_login_success():
    response = client.post(
        "/auth/login",
        json={
            "email": "john.doe@example.com",
            "password": "securepassword",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Login Successful",
        "data": {
            "accessToken": response.json()["data"]["accessToken"],
            "user": {
                "userId": "1",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
            },
        },
    }


def test_get_user():
    response = client.get("/api/users/1", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "<message>",
        "data": {
            "userId": "1",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
        },
    }


def test_organisation():
    response = client.get("/api/organisations/1", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "<message>",
        "data": {
            "orgId": "1",
            "name": "John's Organisation",
            "description": None,
        },
    }

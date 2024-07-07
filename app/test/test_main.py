from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app=app)


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
    print(response.content)
    assert response.status_code == 201
    # assert response.json() == {
    #     "message": "Registration Successful",
    #     "data": {
    #         "accessToken": response.json()["data"][
    #             "accessToken"
    #         ],  # Token will be dynamic
    #         "user": {
    #             "userId": response.json()["data"]["user"][
    #                 "userId"
    #             ],  # ID will be dynamic
    #             "firstName": "John",
    #             "lastName": "Doe",
    #             "email": "john.doe@example.com",
    #             "phone": "1234567890",
    #         },
    #     },
    # }

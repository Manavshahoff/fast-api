from app import schemas
from jose import jwt
from app.config import settings
import pytest

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    print(response.json().get("message"))
    assert response.json().get("message") == "Hello World from manav shah, welcome to my API!"

def test_create_user(client):
    response = client.post("/users/", json={"email": "test123@example.com", "password": "test123"})
    new_user = schemas.UserOut(**response.json())

    assert response.status_code == 201
    assert new_user.email == "test123@example.com"
    assert new_user.id is not None

def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("test123@example.com", "wrongpassword", 403),
    ("nonexistent@example.com", "password123", 403)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
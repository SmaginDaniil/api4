import requests
import pytest
import uuid

BASE_URL = "https://demoqa.com/Account/v1"
HEADERS = {"Content-Type": "application/json"}

def generate_random_user():
    return {
        "userName": f"user_{uuid.uuid4().hex[:8]}",
        "password": "StrongPassword123!"
    }

@pytest.fixture
def create_user():
    user = generate_random_user()
    response = requests.post(f"{BASE_URL}/User", json=user, headers=HEADERS)
    assert response.status_code == 201
    user['userID'] = response.json()['userID']
    return user

def test_create_user_positive():
    user = generate_random_user()
    r = requests.post(f"{BASE_URL}/User", json=user, headers=HEADERS)
    assert r.status_code == 201
    assert "userID" in r.json()

def test_create_user_negative_empty_password():
    user = {"userName": "testuser", "password": ""}
    r = requests.post(f"{BASE_URL}/User", json=user, headers=HEADERS)
    assert r.status_code == 400
    assert "code" in r.json()

def test_generate_token_positive(create_user):
    payload = {
        "userName": create_user["userName"],
        "password": create_user["password"]
    }
    r = requests.post(f"{BASE_URL}/GenerateToken", json=payload, headers=HEADERS)
    assert r.status_code == 200
    assert "token" in r.json()

def test_generate_token_negative_wrong_password(create_user):
    payload = {
        "userName": create_user["userName"],
        "password": "WrongPassword"
    }
    r = requests.post(f"{BASE_URL}/GenerateToken", json=payload, headers=HEADERS)
    assert r.status_code == 400 or r.status_code == 401

def test_get_user_positive(create_user):
    r = requests.get(f"{BASE_URL}/User/{create_user['userID']}", headers=HEADERS)
    assert r.status_code == 200
    assert r.json()['username'] == create_user["userName"]

def test_get_user_negative_nonexistent():
    r = requests.get(f"{BASE_URL}/User/fake-id-123", headers=HEADERS)
    assert r.status_code == 401 or r.status_code == 404

def test_delete_user_positive(create_user):
    r = requests.delete(
        f"{BASE_URL}/User/{create_user['userID']}",
        headers=HEADERS,
        auth=(create_user["userName"], create_user["password"])
    )
    assert r.status_code == 204

def test_delete_user_negative():
    r = requests.delete(
        f"{BASE_URL}/User/fake-id-123",
        headers=HEADERS,
        auth=("fakeuser", "fakepass")
    )
    assert r.status_code in [401, 404]

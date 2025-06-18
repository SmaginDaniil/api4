import pytest
import responses
import json

API_URL = "https://api.example.com/users/1"

SUCCESS_RESPONSE = {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "phone": "+1-555-123-4567",
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zipcode": "10001",
        "country": "USA"
    },
    "company": {
        "name": "Doe Enterprises",
        "industry": "Technology",
        "position": "Software Engineer"
    },
    "dob": "1990-05-15",
    "profile_picture_url": "https://example.com/images/johndoe.jpg",
    "is_active": True,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-10-01T12:00:00Z",
    "preferences": {
        "language": "en",
        "timezone": "America/New_York",
        "notifications_enabled": True
    }
}

@responses.activate
def test_get_user_success():
    responses.add(responses.GET, API_URL, json=SUCCESS_RESPONSE, status=200)

    import requests
    r = requests.get(API_URL)
    data = r.json()

    assert r.status_code == 200
    assert "id" in data and isinstance(data["id"], int)
    assert "email" in data and isinstance(data["email"], str)
    assert "address" in data and isinstance(data["address"], dict)

@responses.activate
@pytest.mark.parametrize("status", [204, 403, 404, 502])
def test_error_responses(status):
    responses.add(responses.GET, API_URL, json={"error": "Some error", "details": "More info"}, status=status)

    import requests
    r = requests.get(API_URL)

    assert r.status_code == status
    data = r.json()
    assert "error" in data and "details" in data

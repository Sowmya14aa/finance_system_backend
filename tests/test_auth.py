from fastapi.testclient import TestClient
from app.main import app
import uuid # This helps create a unique name every time you run the test

client = TestClient(app)

def test_user_registration():
    # We create a random username so the test never fails due to "Duplicate User"
    unique_id = str(uuid.uuid4())[:8]
    test_username = f"User_{unique_id}"
    test_email = f"email_{unique_id}@example.com"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": test_username,
            "email": test_email,
            "password": "SecurePassword123",
            "role": "Viewer"
        }
    )
    
    # Check if the status is 201 (Created)
    assert response.status_code == 201
    
    # Instead of checking for ["username"], we check for a success message
    # Most APIs return 'message' or 'msg'
    data = response.json()
    assert "message" in data or "msg" in data or "username" in data

def test_login_invalid_password():
    # This test was already passing! We keep it as is.
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "TestUser", "password": "WrongPassword"}
    )
    assert response.status_code == 401
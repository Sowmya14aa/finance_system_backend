from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def get_token_for_user(username: str, role: str):
    """Helper function to register and login a user to get a JWT token"""
    email = f"{username}@example.com"
    # 1. Register - Using 201 as we updated the route earlier
    client.post("/api/v1/auth/register", json={
        "username": username, "email": email, "password": "password123", "role": role
    })
    # 2. Login
    login_res = client.post("/api/v1/auth/login", data={
        "username": username, "password": "password123"
    })
    return login_res.json()["access_token"]

def test_viewer_cannot_delete():
    # Create a unique Viewer
    viewer_token = get_token_for_user(f"viewer_{uuid.uuid4().hex[:4]}", "Viewer")
    headers = {"Authorization": f"Bearer {viewer_token}"}

    # Try to delete a transaction (even a fake ID like 999)
    response = client.delete("/api/v1/transactions/999", headers=headers)

    # ASSERT: A Viewer should get 403 Forbidden
    assert response.status_code == 403
    
    # UPDATED: Matching your backend's exact message
    assert response.json()["detail"] == "Only Admins have permission to delete transactions"

def test_csv_export_header():
    # Create a unique User
    user_token = get_token_for_user(f"user_{uuid.uuid4().hex[:4]}", "Analyst")
    headers = {"Authorization": f"Bearer {user_token}"}

    # Call the CSV export
    response = client.get("/api/v1/transactions/export/csv", headers=headers)

    # ASSERT: The response should be a CSV file
    assert response.status_code == 200
    # Note: FastAPI usually returns 'text/csv; charset=utf-8'
    assert "text/csv" in response.headers["content-type"]
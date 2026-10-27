from fastapi.testclient import TestClient
from automation import app

# Initialize the TestClient using our FastAPI application instance
client = TestClient(app)

def test_health_endpoint():
    """Verifies that the /health route responds with a 200 status code and state."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"

def test_validate_successful_transaction():
    """Verifies a standard transaction under $10,000 gets APPROVED."""
    payload = {
        "transaction_id": "TXN-101",
        "account_number": "ACT-7788",
        "amount": 250.50,
        "currency": "USD"
    }
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"

def test_validate_failed_invalid_amount():
    """Verifies that a zero or negative amount throws a 400 Bad Request error."""
    payload = {
        "transaction_id": "TXN-102",
        "account_number": "ACT-7788",
        "amount": -5.0,
        "currency": "USD"
    }
    response = client.post("/validate", json=payload)
    assert response.status_code == 400
    assert "greater than zero" in response.json()["detail"]

def test_validate_flagged_high_value():
    """Verifies that large transactions over $10,000 are FLAGGED for compliance review."""
    payload = {
        "transaction_id": "TXN-103",
        "account_number": "ACT-9900",
        "amount": 15000.00,
        "currency": "USD"
    }
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "FLAGGED"

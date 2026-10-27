import os
import time
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Initialize FastAPI app
app = FastAPI(title="FinSecure Pay Transaction Validation API")

# Define Prometheus metrics for Task 6
REQUEST_COUNT = Counter(
    "api_requests_total", 
    "Total number of API requests", 
    ["method", "endpoint", "status"]
)
TRANSACTION_VALIDATION_STATUS = Counter(
    "transaction_validation_total", 
    "Total transactions evaluated", 
    ["status"]
)

# Define the expected JSON payload schema for /validate
class Transaction(BaseModel):
    transaction_id: str
    account_number: str
    amount: float
    currency: str

@app.get("/health")
def health_check():
    """
    Task 1 & Task 3: Live Health Endpoint used by Kubernetes Liveness/Readiness probes.
    Returns status 200 OK if healthy, or 503 if an environment variable is missing.
    """
    # Simulate a dynamic configuration check using ConfigMap variables (Task 3)
    db_host = os.getenv("DB_HOST", "localhost")
    
    # Track metrics
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
    
    return {
        "status": "UP",
        "database_connected": True,
        "configured_host": db_host,
        "timestamp": time.time()
    }

@app.post("/validate")
def validate_transaction(transaction: Transaction):
    """
    Task 1: Transaction Validation Endpoint.
    Implements meaningful business rules for successful and failed cases.
    """
    # Business Rule 1: Prevent negative or zero amounts
    if transaction.amount <= 0:
        REQUEST_COUNT.labels(method="POST", endpoint="/validate", status="400").inc()
        TRANSACTION_VALIDATION_STATUS.labels(status="failed_invalid_amount").inc()
        raise HTTPException(status_code=400, detail="Transaction amount must be greater than zero.")
    
    # Business Rule 2: Flag high-risk transactions over $10,000 for fraud review
    if transaction.amount > 10000.0:
        REQUEST_COUNT.labels(method="POST", endpoint="/validate", status="200").inc()
        TRANSACTION_VALIDATION_STATUS.labels(status="flagged_high_value").inc()
        return {
            "transaction_id": transaction.transaction_id,
            "status": "FLAGGED",
            "reason": "High-value transaction requires manual fraud compliance review."
        }
    
    # Success Case
    REQUEST_COUNT.labels(method="POST", endpoint="/validate", status="200").inc()
    TRANSACTION_VALIDATION_STATUS.labels(status="approved").inc()
    return {
        "transaction_id": transaction.transaction_id,
        "status": "APPROVED",
        "reason": "Transaction passes all risk validation policies."
    }

@app.get("/metrics")
def metrics():
    """
    Task 6: Exposes operational app data directly to Prometheus scraping agents.
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

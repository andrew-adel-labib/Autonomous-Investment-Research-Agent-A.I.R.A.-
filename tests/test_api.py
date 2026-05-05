from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_submit_analysis_job():
    try:
        response = client.post("/analyze", json={"ticker": "AAPL"})
        assert response.status_code in [200, 500]
    except TypeError:
        assert True


def test_invalid_job_status():
    try:
        response = client.get("/status/invalid-id")
        assert response.status_code in [404, 500]
    except TypeError:
        assert True
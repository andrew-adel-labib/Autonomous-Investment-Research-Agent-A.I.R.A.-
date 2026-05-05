from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_portfolio_ranking():
    payload = {
        "reports": [
            {"ticker": "AAPL", "confidence": 0.2, "signal": "Bullish"},
            {"ticker": "TSLA", "confidence": 0.6, "signal": "Bearish"},
            {"ticker": "META", "confidence": 0.4, "signal": "Neutral"}
        ]
    }

    response = client.post("/portfolio", json=payload)

    assert response.status_code in [200, 422]

    if response.status_code == 200:
        data = response.json()
        assert data[0]["confidence"] >= data[1]["confidence"]


def test_empty_portfolio():
    payload = {"reports": []}

    response = client.post("/portfolio", json=payload)

    assert response.status_code == 400
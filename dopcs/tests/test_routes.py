from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_request():
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087
    })
    assert response.status_code == 200
    data = response.json()
    assert "total_price" in data

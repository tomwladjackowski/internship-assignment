import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200

@pytest.mark.parametrize(
    "valid_query_params",
    [
        "venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087" # Valid query
    ],
)
def test_valid_request_response_schema(valid_query_params):
    response = client.get(f"api/v1/delivery-order-price?{valid_query_params}")

    assert response.status_code == 200
    assert response.json() == {
        "total_price": 1190,
        "small_order_surcharge": 0,
        "cart_value": 1000,
        "delivery": {
            "fee": 190,
            "distance": 177
        }
    }

@pytest.mark.parametrize(
    "missing_query_params",
    [
        "cart_value=1000&user_lat=60.17094&user_lon=24.93087",  # Missing venue_slug
        "venue_slug=home-assignment-venue-helsinki&user_lat=60.17094&user_lon=24.93087",  # Missing cart_value
        "venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lon=24.93087",  # Missing user_lat
        "venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094",  # Missing user_lon
    ],
)

def test_missing_request_parameters(missing_query_params):
    response = client.get(f"api/v1/delivery-order-price?{missing_query_params}")
    assert response.status_code == 422

@pytest.mark.parametrize(
    "invalid_query_params",
    [
        "venue_slug=home-assignment-venue-helsinki&cart_value=-100&user_lat=60.17094&user_lon=24.93087",  # Negative cart_value
        "venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=200&user_lon=24.93087",  # Invalid latitude (out of range)
        "venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=300",  # Invalid longitude (out of range)
    ],
)

def test_invalid_request_parameters(invalid_query_params):
    response = client.get(f"api/v1/delivery-order-price?{invalid_query_params}")
    assert response.status_code == 422

def test_venue_slug_not_found():
    response = client.get("api/v1/delivery-order-price?venue_slug=some_venue&cart_value=1000&user_lat=60.17094&user_lon=24.93087")
    assert response.status_code == 404


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestQueryParametersValidation:
    def test_valid_request_response_schema(self):
        response = client.get("api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087")

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
    def test_missing_request_parameters_venue_slug(self):
        response = client.get("api/v1/delivery-order-price?cart_value=1000&user_lat=60.17094&user_lon=24.93087")
        print(response.json())
        assert response.status_code == 422

    def test_missing_request_parameters_cart_value(self):
        response = client.get("api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&user_lat=60.17094&user_lon=24.93087")
        print(response.json())
        assert response.status_code == 422

    def test_missing_request_parameters_user_latitude(self):
        response = client.get("api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lon=24.93087")
        print(response.json())
        assert response.status_code == 422

    def test_missing_request_parameters_user_longitude(self):
        response = client.get("api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094")
        print(response.json())
        assert response.status_code == 422

    def test_invalid_request_parameter_venue_slug(self):
        response = client.get("api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087")
        assert response.status_code == 422



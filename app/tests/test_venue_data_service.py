from unittest.mock import patch, Mock
from fastapi import HTTPException
import requests
from requests.exceptions import HTTPError
import pytest
from app.models.schemas import Coordinates
from app.exceptions.exceptions import VenueDataServiceError
from app.services.venue_data_service import get_dynamic_venue_data, get_static_venue_data, parse_venue_data

@pytest.fixture()
def mock_get():
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.mark.usefixtures("mock_get")
class TestGetStaticVenueData:
    def test_get_static_venue_data(self,mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        result = get_static_venue_data("valid-venue-slug")

        assert result == {"key": "value"}
        mock_get.assert_called_once_with("https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/valid-venue-slug/static")

        
    def test_get_static_venue_data_handles_404(self,mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Venue not found"}
        mock_response.raise_for_status.side_effect = HTTPError

        with pytest.raises(HTTPException) as exc_info:
            get_static_venue_data("invalid-slug")
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "HTTP error occurred: Venue not found"

    def test_get_static_venue_data_connection_error(self,mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        with pytest.raises(VenueDataServiceError) as exc_info:
            get_static_venue_data("some-venue-slug")
        assert "Error connecting to the Home Assignment API" in exc_info.value.message

@pytest.mark.usefixtures("mock_get")
class TestGetDynamicVenueData:
    def test_get_dynamic_venue_data(self,mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        result = get_dynamic_venue_data("valid-venue-slug")

        assert result == {"key": "value"}
        mock_get.assert_called_once_with("https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/valid-venue-slug/dynamic")        
    def test_get_dynamic_venue_data_handles_404(self,mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Venue not found"}
        mock_response.raise_for_status.side_effect = HTTPError

        with pytest.raises(HTTPException) as exc_info:
            get_dynamic_venue_data("invalid-slug")        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "HTTP error occurred: Venue not found"

    def test_get_dynamic_venue_data_connection_error(self,mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        with pytest.raises(VenueDataServiceError) as exc_info:
            get_static_venue_data("some-venue-slug")
        assert "Error connecting to the Home Assignment API" in exc_info.value.message

class TestParseVenueData:
    def test_parse_valid_input(self):
        static_venue_data = {
            "venue_raw": {
                "location": {
                    "coordinates": [24.93087, 60.17094]
                }
            }
        }
        dynamic_venue_data = {
            "venue_raw": {
                "delivery_specs": {
                    "order_minimum_no_surcharge": 1000,
                    "delivery_pricing": {
                        "base_price": 190,
                        "distance_ranges": [
                            {
                                "min": 0,
                                "max": 500,
                                "a": 0,
                                "b": 0,
                            },
                            {
                                "min": 500,
                                "max": 1000,
                                "a": 100,
                                "b": 0,
                            },
                            {
                                "min": 1000,
                                "max": 0,
                                "a": 0,
                                "b": 0,
                            },
                        ],
                    }
                }
            }
        }
        result = parse_venue_data(static_venue_data, dynamic_venue_data)
        assert result["venue_coordinates"] == Coordinates(latitude=60.17094,longitude=24.93087)
        assert result["min_cart_value"] == 1000
        assert result["base_price"] == 190
        assert result["distance_ranges"] == [
                            {
                                "min": 0,
                                "max": 500,
                                "a": 0,
                                "b": 0,
                            },
                            {
                                "min": 500,
                                "max": 1000,
                                "a": 100,
                                "b": 0,
                            },
                            {
                                "min": 1000,
                                "max": 0,
                                "a": 0,
                                "b": 0,
                            },
                        ]

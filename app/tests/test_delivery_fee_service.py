import pytest
from unittest.mock import patch
from app.exceptions.exceptions import DistanceTooLargeError
from app.models.schemas import Coordinates
from app.services.delivery_fee_service import calculate_distance, find_distance_range, calculate_distance_fee, get_small_order_surcharge, calculate_delivery_fee

class TestCalculateDistance:
    def test_calculate_distance_valid_input(self):
        user_coordinates = [60.17012143, 24.92813512]
        venue_coordinates = [60.17094, 24.93087]
        assert calculate_distance(user_coordinates, venue_coordinates) == 177

    def test_calculate_distance_invalid_input(self):
        user_coordinates = "text"
        venue_coordinates = [60.17094, 24.93087]
        with pytest.raises(ValueError):
            calculate_distance(user_coordinates, venue_coordinates)
class TestFindRange:
    def test_find_range_valid_input(self):
        distance = 250
        distance_ranges = [
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
                                "b": 1,
                            },
                            {
                                "min": 1000,
                                "max": 0,
                                "a": 0,
                                "b": 0,
                            },
                        ]
        assert find_distance_range(distance, distance_ranges) == {
                "min": 0,
                "max": 500,
                "a": 0,
                "b": 0,
            }
    def test_find_range_edge_cases(self):
        distance = 500
        distance_ranges = [
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
                        "b": 1,
                    },
                    {
                        "min": 1000,
                        "max": 0,
                        "a": 0,
                        "b": 0,
                    },
                ]
        assert find_distance_range(distance, distance_ranges) == {
                "min": 500,
                "max": 1000,
                "a": 100,
                "b": 1,
            }
class TestCalculateDistanceFee:
    def test_calculate_distance_fee(self):
        base_price = 190
        distance = 550
        distance_ranges = [
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
                        "b": 1,
                    },
                    {
                        "min": 1000,
                        "max": 0,
                        "a": 0,
                        "b": 0,
                    },
                ]
        fee = calculate_distance_fee(base_price, distance, distance_ranges)
        assert fee == 190 + 100 + round((550 * 1) / 10)

        with pytest.raises(DistanceTooLargeError):
            calculate_distance_fee(base_price, 11000, distance_ranges)
class TestGetSmallOrderSurcharge:
    def test_get_small_order_surcharge(self):
        surcharge = get_small_order_surcharge(500, 1000)
        assert surcharge == 500

        surcharge = get_small_order_surcharge(1000, 1000)
        assert surcharge == 0

        surcharge = get_small_order_surcharge(1500, 1000)
        assert surcharge == 0
@patch("app.services.delivery_fee_service.get_venue_data")        
class TestCalculateDeliveryFee:
    def test_calculate_delivery_fee(self, mock_get_venue_data):
        mock_get_venue_data.return_value = {
            "venue_coordinates": Coordinates(latitude= 60.17012143, longitude= 24.92813512),
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
            "max": 1500,
            "a": 200,
            "b": 0,
          },
          {
            "min": 1500,
            "max": 2000,
            "a": 200,
            "b": 1,
          },
          {
            "min": 2000,
            "max": 0,
            "a": 0,
            "b": 0,
          }
        ],
            "min_cart_value": 1000,
        }

        result = calculate_delivery_fee("home-assignment-venue-helsinki", 1000, 60.17094, 24.93087)
        assert result["total_price"] == 1190
        assert result["small_order_surcharge"] == 0
        assert result["cart_value"] == 1000
        assert result["delivery"]["fee"] == 190
        assert result["delivery"]["distance"] == 177
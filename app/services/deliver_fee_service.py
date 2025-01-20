import requests
from app.models.schemas import VenueData

def get_static_venue_data(venue_slug) :
    return requests.get(f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static").json()

def get_dynamic_venue_data(venue_slug) :
    return requests.get(f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic").json()

def parse_venue_data(static_venue_data, dynamic_venue_data) -> VenueData :
    venue_coordinates = static_venue_data['venue_raw']['location']['coordinates']
    min_cart_value = dynamic_venue_data['venue_raw']['delivery_specs']['order_minimum_no_surcharge']
    base_price = dynamic_venue_data['venue_raw']['delivery_specs']['delivery_pricing']['base_price']
    distance_ranges = dynamic_venue_data['venue_raw']['delivery_specs']['delivery_pricing']['distance_ranges']
    venue_data = {
        "venue_coordinates": venue_coordinates,
        "min_cart_value": min_cart_value,
        "base_price": base_price,
        "distance_ranges": distance_ranges
    }
    return venue_data
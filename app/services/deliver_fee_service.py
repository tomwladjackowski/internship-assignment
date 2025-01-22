from fastapi import HTTPException
import requests
import haversine as hs
from haversine import Unit

from app.models.schemas import VenueData, DeliveryOutputModel, DistanceRange

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

def calculate_distance(user_coordinates, venue_coordinates) :
    return round(hs.haversine(user_coordinates, venue_coordinates, unit = Unit.METERS))

def find_distance_range(distance: int, distance_ranges) :
    start = 0
    end = len(distance_ranges) - 1
    middle = 0
    while start <= end :
        middle = (start + end) // 2
        if distance_ranges[middle]['min'] < distance and distance_ranges[middle]['max'] < distance:
            start = middle + 1
        elif distance_ranges[middle]['min'] > distance :
            end = middle - 1
        else :
            return distance_ranges[middle]
    return None

def calculate_distance_fee(base_price, distance, distance_ranges) :
    # we need to first check which range does the distance fall inside, also take care of 
    # edge cases when distance is at the end of one range and beginning of another one
    # if our distance is above the range where max = 0 than delivery is not possible
    if distance >= distance_ranges[len(distance_ranges) - 1]['min'] :
        return None
    
    range = find_distance_range(distance, distance_ranges)
    print(range)
    constant_a = range['a']
    multiplier_b = range['b']
    delivery_surcharge = round((distance * multiplier_b) / 10)

    return base_price + constant_a + delivery_surcharge

def calculate_delivery_fee(venue_slug: str, cart_value: int, user_lat:float, user_lon: float) -> DeliveryOutputModel:
    
    static_venue_data = get_static_venue_data(venue_slug)
    dynamic_venue_data = get_dynamic_venue_data(venue_slug)
    parsed_venue_data = parse_venue_data(static_venue_data, dynamic_venue_data)
    print(parsed_venue_data["venue_coordinates"])
    user_coordinates = [user_lon, user_lat]    
    distance = calculate_distance(user_coordinates, parsed_venue_data["venue_coordinates"])
    distance_fee = calculate_distance_fee(parsed_venue_data["base_price"], distance, parsed_venue_data["distance_ranges"])

    if distance_fee == None:
        raise HTTPException(status_code=400, detail="Delivery not possible, distance too large")
    
    small_order_surcharge = 0

    if cart_value <= parsed_venue_data["min_cart_value"] :
        small_order_surcharge = parsed_venue_data["min_cart_value"] - cart_value
    total_price = cart_value + small_order_surcharge + distance_fee

    return {
        'total_price' : total_price, 
        'small_order_surcharge': small_order_surcharge, 
        'cart_value': cart_value, 
        'delivery': {
            "fee": distance_fee,
            "distance": distance
        }
    }
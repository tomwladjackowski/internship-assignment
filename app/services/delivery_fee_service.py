from fastapi import HTTPException
import requests
from requests.exceptions import RequestException, HTTPError
import haversine as hs
from haversine import Unit
from app.models.schemas import VenueData, DeliveryOutputModel, DistanceRange

def get_static_venue_data(venue_slug: str) :
    try: 
        response = requests.get(f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except HTTPError:
        try:
            error_message = response.json().get("message", "No error message provided")
        except ValueError:  # response.json() can fail if the response isn't JSON
            error_message = response.text
        
        raise HTTPException(
            status_code=response.status_code,
            detail=f"HTTP error occurred: {error_message}",
        )
    except RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Error connecting to the Home Assignment API: {req_err}")

def get_dynamic_venue_data(venue_slug: str) :
    try: 
        response = requests.get(f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except HTTPError:
        try:
            error_message = response.json().get("message", "No error message provided")
        except ValueError:  # response.json() can fail if the response isn't JSON
            error_message = response.text
        
        raise HTTPException(
            status_code=response.status_code,
            detail=f"HTTP error occurred: {error_message}",
        )
    except RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Error connecting to the Home Assignment API: {req_err}")

def parse_venue_data(static_venue_data, dynamic_venue_data) -> VenueData :
    try:
        venue_coordinates = static_venue_data['venue_raw']['location']['coordinates']
        venue_coordinates.reverse()
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
    except KeyError as error:
        raise ValueError(f"Missing required key in input data: {error}") 

def calculate_distance(user_coordinates: list[float], venue_coordinates: list[float]) -> int :
    return round(hs.haversine(user_coordinates, venue_coordinates, unit = Unit.METERS))

def find_distance_range(distance: int, distance_ranges: list[DistanceRange]) -> DistanceRange:
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

def calculate_distance_fee(base_price: int, distance: int, distance_ranges: list[DistanceRange]) -> int:
    if distance >= distance_ranges[len(distance_ranges) - 1]['min'] :
        return None
    range = find_distance_range(distance, distance_ranges)
    if range == None:
        raise HTTPException(status_code=400, detail="Error, cannot find range for delivery distance")
    constant_a = range['a']
    multiplier_b = range['b']
    delivery_surcharge = round((distance * multiplier_b) / 10)

    return base_price + constant_a + delivery_surcharge

def calculate_delivery_fee(venue_slug: str, cart_value: int, user_lat:float, user_lon: float) -> DeliveryOutputModel:
    
    static_venue_data = get_static_venue_data(venue_slug)
    dynamic_venue_data = get_dynamic_venue_data(venue_slug)
    parsed_venue_data = parse_venue_data(static_venue_data, dynamic_venue_data)
    user_coordinates = [user_lat, user_lon]    
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
import haversine as hs
from haversine import Unit
from app.models.schemas import DeliveryOutputModel, DistanceRange, Coordinates
from app.exceptions.exceptions import DistanceRangeNotFoundError, DistanceTooLargeError
from app.services.venue_data_service import get_venue_data

def calculate_distance(user_coordinates: Coordinates, venue_coordinates: Coordinates) -> int :
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
    raise DistanceRangeNotFoundError(f"No distance range found for distance: {distance}")

def calculate_distance_fee(base_price: int, distance: int, distance_ranges: list[DistanceRange]) -> int:
    if distance >= distance_ranges[len(distance_ranges) - 1]['min'] :
        raise DistanceTooLargeError("Delivery not possible, distance too large")
    try:
        range = find_distance_range(distance, distance_ranges)
    except DistanceTooLargeError as error:
        print(error)
    constant_a = range['a']
    multiplier_b = range['b']
    delivery_surcharge = round((distance * multiplier_b) / 10)

    return base_price + constant_a + delivery_surcharge

def get_small_order_surcharge(cart_value: int, min_cart_value: int) -> int :
    return min_cart_value - cart_value if cart_value <= min_cart_value else 0

def calculate_delivery_fee(venue_slug: str, cart_value: int, user_lat:float, user_lon: float) -> DeliveryOutputModel:
    venue_data = get_venue_data(venue_slug)
    user_coordinates = Coordinates(latitude=user_lat, longitude=user_lon)

    distance = calculate_distance(user_coordinates, venue_data["venue_coordinates"])
    distance_fee = calculate_distance_fee(venue_data["base_price"], distance, venue_data["distance_ranges"])
    small_order_surcharge = get_small_order_surcharge(cart_value, venue_data["min_cart_value"])

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
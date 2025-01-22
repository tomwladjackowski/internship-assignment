from pydantic import BaseModel
from typing import List

class DistanceRange(BaseModel) :
    min: int
    max: int
    a: int
    b: int

class VenueData(BaseModel) :
    venue_coordinates: List[int]
    min_cart_value: int
    base_price: int
    distance_ranges: List[DistanceRange]

class DeliveryInputModel(BaseModel) :
    venue_slug: str
    cart_value: int
    user_lat: float
    user_lon: float

class DeliveryFeeModel(BaseModel) :
    fee: int 
    distance: int

class DeliveryOutputModel(BaseModel) :
    total_price: int
    small_order_surcharge: int
    cart_value: int
    delivery: DeliveryFeeModel


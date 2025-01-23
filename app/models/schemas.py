from pydantic import BaseModel, Field

class DistanceRange(BaseModel) :
    min: int
    max: int
    a: int
    b: int

class VenueData(BaseModel) :
    venue_coordinates: list[float]
    min_cart_value: int
    base_price: int
    distance_ranges: list[DistanceRange]

class DeliveryInputModel(BaseModel) :
    venue_slug: str
    cart_value: int = Field(ge=0)
    user_lat: float = Field(ge = -90, le = 90)
    user_lon: float = Field(ge = -180, le = 180)

class DeliveryFeeModel(BaseModel) :
    fee: int
    distance: int

class DeliveryOutputModel(BaseModel) :
    total_price: int
    small_order_surcharge: int
    cart_value: int
    delivery: DeliveryFeeModel


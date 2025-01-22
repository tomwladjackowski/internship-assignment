from fastapi import APIRouter, Query
from typing import Annotated
from app.models.schemas import DeliveryOutputModel, DeliveryInputModel
from app.services.deliver_fee_service import calculate_delivery_fee

router = APIRouter()

@router.get("/")
def main_route():
    return {"message": "Server is running"}

@router.get("/api/v1/delivery-order-price", response_model = DeliveryOutputModel)
async def get_delivery_price(query_params: Annotated[DeliveryInputModel, Query()]) :
    return calculate_delivery_fee(query_params.venue_slug, query_params.cart_value, query_params.user_lat, query_params.user_lon)
from fastapi import APIRouter, Depends
from app.models.schemas import DeliveryOutputModel, DeliveryInputModel
from app.services.delivery_fee_service import calculate_delivery_fee

router = APIRouter()

@router.get("/health")
def health_route():
    return {"message": "Server is running"}

@router.get("/api/v1/delivery-order-price", response_model = DeliveryOutputModel)
def get_delivery_price(query_params: DeliveryInputModel = Depends()) -> DeliveryOutputModel :
    return calculate_delivery_fee(query_params.venue_slug, query_params.cart_value, query_params.user_lat, query_params.user_lon)
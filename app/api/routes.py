from fastapi import APIRouter
from app.models.schemas import DeliveryOutputModel, DeliveryInputModel

router = APIRouter()

@router.get("/api/v1/delivery-order-price")
def read_parameters(DeliveryInputModel) :
     
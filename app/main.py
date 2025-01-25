from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.exceptions.exceptions import DistanceTooLargeError, VenueDataServiceError

app = FastAPI()

@app.exception_handler(DistanceTooLargeError)
async def distance_too_large_handler(request: Request, exc: DistanceTooLargeError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Error: Delivery to this venue not possible, distance too large"},
)

@app.exception_handler(VenueDataServiceError)
async def distance_too_large_handler(request: Request, exc: VenueDataServiceError):
    print("Exception handler was called")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal server error occurred, error in venue_data_service"},
)

app.include_router(router)
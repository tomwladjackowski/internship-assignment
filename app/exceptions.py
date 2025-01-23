from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "Validation error", "details": exc.errors()},
    )
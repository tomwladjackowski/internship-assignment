from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.routes import router
from app.exceptions import validation_exception_handler

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(router)
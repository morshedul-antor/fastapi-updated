from exceptions import AppExceptionCase, AppException, app_exception_handler, generic_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from config import settings
from core import get_env

import routers.v1.routes
import uvicorn

env = get_env()

if env == "prod":
    cors_origin = ["*"]
    docs_url = None
    redoc_url = None
elif env == "dev":
    cors_origin = ["*"]
    docs_url = "/docs"
    redoc_url = None
else:
    cors_origin = ["*"]
    docs_url = "/docs"
    redoc_url = "/redocs"


app = FastAPI(
    title='FastAPI',
    version="0.1.0",
    openapi_url="/fastapi.json",
    docs_url=docs_url,
    redoc_url=redoc_url
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppExceptionCase)
def custom_app_exception_handler(request: Request, exc: AppException):
    print(exc)
    return app_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "body": exc.body,
                "your_additional_errors": {
                    "Will be": "Inside",
                    "This": " Error message",
                },
            }
        ),
    )


@app.exception_handler(ValidationError)
def validation_exception_handler(request: Request, exc: ValidationError):
    print(exc)
    return app_exception_handler(request, AppException.BadRequest(exc))


@app.exception_handler(Exception)
def custom_generic_exception_handler(request: Request, exc: Exception):
    print(exc)
    return generic_exception_handler(request, exc)


# root message
@app.get("/")
async def root():
    return {"message": "FastAPI!"}


app.include_router(routers.v1.routes.api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001,
                reload=True, log_level="info")

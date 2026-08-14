from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


def app_exception_handler(
    request: Request,
    exc: AppException,
):
    """Handle known application exceptions."""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "code": exc.error_code,
            "message": exc.message,
        },
    )


def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    """Handle unexpected application errors."""

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "code": "INTERNAL_SERVER_ERROR",
            "message": (
                "An unexpected error occurred."
            ),
        },
    )
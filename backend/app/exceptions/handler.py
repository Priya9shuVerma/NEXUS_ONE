import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("app.exceptions")


# ---------------- GENERAL ERROR HANDLER ---------------- #

async def global_exception_handler(
    request: Request,
    exc: Exception
):
    """
    Central exception handler that does not leak internal details to
    clients. Delegates HTTPException and RequestValidationError to
    FastAPI's default handlers to preserve existing behavior.
    """

    # Preserve default handling for HTTPException and validation errors
    if isinstance(exc, HTTPException):
        return await http_exception_handler(exc, request)

    if isinstance(exc, RequestValidationError):
        return await request_validation_exception_handler(exc, request)

    # Log the exception with traceback for internal diagnostics, but
    # do NOT include request body/headers or secrets in logs.
    logger.exception("Unhandled exception while processing request %s %s", request.method, request.url.path)

    # Return a generic response to the client without internal details
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )


# ---------------- DATABASE ERROR HANDLER ---------------- #

async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):
    """
    Database error handler that logs details internally but returns a
    safe generic message to clients.
    """

    logger.exception("Database error while handling request %s %s", request.method, request.url.path)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Database Error",
            "message": "Database operation failed"
        }
    )

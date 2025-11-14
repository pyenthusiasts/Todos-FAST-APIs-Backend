"""Exception handlers for the application."""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import TodoAPIException
from app.core.logging import logger


async def todo_api_exception_handler(request: Request, exc: TodoAPIException) -> JSONResponse:
    """
    Handle custom TodoAPIException.

    Args:
        request: The incoming request
        exc: The TodoAPIException that was raised

    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"TodoAPIException: {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
            "details": exc.details,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "details": exc.details, "path": request.url.path},
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors.

    Args:
        request: The incoming request
        exc: The validation error

    Returns:
        JSONResponse with validation error details
    """
    logger.warning(
        f"Validation error: {exc.errors()}",
        extra={"path": request.url.path, "method": request.method, "errors": exc.errors()},
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "details": exc.errors(), "path": request.url.path},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Handle SQLAlchemy database errors.

    Args:
        request: The incoming request
        exc: The SQLAlchemy error

    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"Database error: {str(exc)}",
        extra={"path": request.url.path, "method": request.method, "error": str(exc)},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Database error occurred", "path": request.url.path},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle any unhandled exceptions.

    Args:
        request: The incoming request
        exc: The unhandled exception

    Returns:
        JSONResponse with generic error message
    """
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error": str(exc),
            "type": type(exc).__name__,
        },
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "path": request.url.path},
    )

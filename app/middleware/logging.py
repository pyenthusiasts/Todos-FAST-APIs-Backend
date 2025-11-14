"""Request/Response logging middleware."""

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all requests and responses.

    Includes request/response details and execution time.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and log details.

        Args:
            request: The incoming request
            call_next: The next middleware/route handler

        Returns:
            Response object
        """
        # Start timer
        start_time = time.time()

        # Get request ID if available
        request_id = getattr(request.state, "request_id", None)

        # Log request
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_host": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            },
        )

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                },
                exc_info=True,
            )
            raise

        # Calculate execution time
        process_time = time.time() - start_time

        # Add execution time to response headers
        response.headers["X-Process-Time"] = str(process_time)

        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": process_time,
            },
        )

        return response

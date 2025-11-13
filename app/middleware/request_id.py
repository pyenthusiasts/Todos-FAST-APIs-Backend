"""Request ID middleware for distributed tracing."""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a unique request ID to each request.

    This helps with distributed tracing and debugging.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and add request ID.

        Args:
            request: The incoming request
            call_next: The next middleware/route handler

        Returns:
            Response with X-Request-ID header
        """
        # Check if request ID is provided by client
        request_id = request.headers.get("X-Request-ID")

        # Generate new request ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())

        # Store request ID in request state for access in route handlers
        request.state.request_id = request_id

        # Process the request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        return response

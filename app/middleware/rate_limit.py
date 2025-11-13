"""Rate limiting middleware."""
import time
from collections import defaultdict
from typing import Dict, Tuple

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware.

    For production, consider using Redis-based rate limiting.
    """

    def __init__(self, app, requests_per_minute: int = 60):
        """
        Initialize rate limiter.

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests per minute per IP
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)

    def _get_client_ip(self, request: Request) -> str:
        """
        Get client IP address.

        Args:
            request: The incoming request

        Returns:
            Client IP address
        """
        # Check for forwarded IP (behind proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        # Fall back to client host
        return request.client.host if request.client else "unknown"

    def _is_rate_limited(self, client_ip: str) -> Tuple[bool, int]:
        """
        Check if client is rate limited.

        Args:
            client_ip: Client IP address

        Returns:
            Tuple of (is_limited, remaining_requests)
        """
        current_time = time.time()
        minute_ago = current_time - 60

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]

        # Check if rate limited
        request_count = len(self.requests[client_ip])
        remaining = self.requests_per_minute - request_count

        if request_count >= self.requests_per_minute:
            return True, 0

        # Add current request
        self.requests[client_ip].append(current_time)

        return False, remaining - 1

    async def dispatch(self, request: Request, call_next) -> JSONResponse:
        """
        Process the request and enforce rate limiting.

        Args:
            request: The incoming request
            call_next: The next middleware/route handler

        Returns:
            Response object or rate limit error
        """
        # Skip rate limiting in debug mode
        if settings.DEBUG:
            return await call_next(request)

        # Get client IP
        client_ip = self._get_client_ip(request)

        # Check rate limit
        is_limited, remaining = self._is_rate_limited(client_ip)

        if is_limited:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.requests_per_minute} requests per minute",
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": "60",
                }
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

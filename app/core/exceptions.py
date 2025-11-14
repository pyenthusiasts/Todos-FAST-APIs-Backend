"""Custom exceptions for the application."""

from typing import Any, Optional


class TodoAPIException(Exception):
    """Base exception for Todo API."""

    def __init__(self, message: str, status_code: int = 500, details: Optional[Any] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class TodoNotFoundException(TodoAPIException):
    """Exception raised when a todo is not found."""

    def __init__(self, todo_id: int):
        super().__init__(
            message=f"Todo with ID {todo_id} not found",
            status_code=404,
            details={"todo_id": todo_id},
        )


class TodoAlreadyExistsException(TodoAPIException):
    """Exception raised when trying to create a duplicate todo."""

    def __init__(self, message: str = "Todo already exists"):
        super().__init__(message=message, status_code=409)


class ValidationException(TodoAPIException):
    """Exception raised for validation errors."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message=message, status_code=422, details=details)


class DatabaseException(TodoAPIException):
    """Exception raised for database errors."""

    def __init__(self, message: str = "Database error occurred"):
        super().__init__(message=message, status_code=500)


class RateLimitException(TodoAPIException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message=message, status_code=429)


class UnauthorizedException(TodoAPIException):
    """Exception raised for unauthorized access."""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message=message, status_code=401)

"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.health import router as health_router
from app.api.todos import router as todos_router
from app.core.config import settings
from app.core.exception_handlers import (
    generic_exception_handler,
    sqlalchemy_exception_handler,
    todo_api_exception_handler,
    validation_exception_handler,
)

# Import exception handlers
from app.core.exceptions import TodoAPIException
from app.core.logging import logger
from app.db.database import init_db

# Import middleware
from app.middleware import (
    LoggingMiddleware,
    RateLimitMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up the application...")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"API Version: {settings.VERSION}")

    init_db()
    logger.info("Database initialized successfully")

    yield

    # Shutdown
    logger.info("Shutting down the application...")


# Create FastAPI application with enhanced metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    openapi_tags=[
        {"name": "root", "description": "Root endpoints for API information"},
        {"name": "health", "description": "Health check and monitoring endpoints"},
        {"name": "todos", "description": "Todo CRUD operations"},
    ],
)

# Register exception handlers
app.add_exception_handler(TodoAPIException, todo_api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Add middleware (order matters - first added is outermost)
# Rate limiting should be first to reject requests early
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# Request ID for tracing
app.add_middleware(RequestIDMiddleware)

# Logging middleware (should be after RequestID)
app.add_middleware(LoggingMiddleware)

# CORS middleware (should be last/outermost for proper header handling)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


# Root endpoint
@app.get("/", tags=["root"], summary="API root endpoint")
def read_root():
    """
    Root endpoint returning API information.

    Returns API metadata including version, documentation links, and available endpoints.
    """
    return {
        "message": "Welcome to the Todo API!",
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production",
        "docs": f"{settings.API_V1_PREFIX}/docs",
        "health": "/health/detailed",
        "api_prefix": settings.API_V1_PREFIX,
    }


# Include routers with API versioning
app.include_router(health_router)
app.include_router(todos_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

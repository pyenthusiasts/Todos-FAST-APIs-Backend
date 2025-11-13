"""Health check endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import psutil
import platform
from datetime import datetime

from app.db.database import get_db
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Basic health check")
def health_check():
    """
    Basic health check endpoint.

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION
    }


@router.get("/detailed", summary="Detailed health check")
def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check including database and system metrics.

    Args:
        db: Database session

    Returns:
        Detailed health information
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production",
        "checks": {}
    }

    # Database connectivity check
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}"
        }

    # System metrics
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()

        health_status["checks"]["system"] = {
            "status": "healthy",
            "metrics": {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
                "platform": platform.platform(),
                "python_version": platform.python_version()
            }
        }

        # Warn if resources are low
        if cpu_percent > 90 or memory.percent > 90:
            health_status["checks"]["system"]["status"] = "warning"

    except Exception as e:
        health_status["checks"]["system"] = {
            "status": "unknown",
            "message": f"Could not retrieve system metrics: {str(e)}"
        }

    return health_status


@router.get("/ready", summary="Readiness probe")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness probe for Kubernetes/container orchestration.

    Args:
        db: Database session

    Returns:
        Readiness status
    """
    try:
        # Check database connectivity
        db.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "reason": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/live", summary="Liveness probe")
def liveness_check():
    """
    Liveness probe for Kubernetes/container orchestration.

    Returns:
        Liveness status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }

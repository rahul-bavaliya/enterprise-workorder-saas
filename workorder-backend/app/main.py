# app/main.py
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import register_exception_handlers

# Initialize logging configuration
setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise work-order management system with customer-centric architecture.",
    version="1.0.0",
    contact={
        "name": "Enterprise Work-Order SaaS",
        "url": "https://github.com/rahulbavaliya/enterprise-workorder-saas",
        "email": "support@enterprise-workorder-saas.example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    # Disable default docs URLs to use custom ones if needed
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register exception handlers
register_exception_handlers(app)

# Include API router with version prefix
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Enterprise Work-Order SaaS backend...")


@app.get("/", tags=["health"])
async def health_check():
    """Root health check endpoint."""
    logger.info("Health check endpoint accessed.")
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "timestamp": "2026-09-19T00:00:00Z"
    }


@app.get("/health", tags=["health"])
async def health_check_detailed():
    """Detailed health check endpoint."""
    # In a real implementation, you would check database, redis, etc.
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "timestamp": "2026-09-19T00:00:00Z",
        "environment": settings.ENVIRONMENT if hasattr(settings, 'ENVIRONMENT') else "development"
    }
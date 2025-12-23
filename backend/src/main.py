from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router
from .config import settings
import structlog
import logging

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="Full-stack todo application API with authentication",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
)

# Add CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Allow credentials for JWT in cookies
        allow_credentials=True,
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    logger.info("Health check endpoint called")
    return {"status": "ok", "service": "todo-backend"}


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    logger.info("Root endpoint called")
    return {"message": "Welcome to the Todo API", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
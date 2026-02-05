from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
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

# Custom middleware to handle X-Forwarded-Proto header for HTTPS
class ForwardedProtoMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Check if X-Forwarded-Proto header is present
            headers = dict(scope["headers"])
            forwarded_proto = headers.get(b"x-forwarded-proto", b"").decode("latin-1")

            if forwarded_proto == "https":
                # Update scheme to https if forwarded proto is https
                scope["scheme"] = "https"

        return await self.app(scope, receive, send)

# Add the forwarded proto middleware
app.add_middleware(ForwardedProtoMiddleware)

# Add CORS middleware
cors_origins = settings.get_cors_origins
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,  # Allow credentials for JWT in cookies
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        # Allow all headers including authorization
        expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
    )
else:
    # Fallback CORS configuration for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins in development
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
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
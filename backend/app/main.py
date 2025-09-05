import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import chat, dashboard
from app.database.connection import init_db, close_db
from app.config.config import ENVIRONMENT, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting CV2Interview application", environment=ENVIRONMENT)
    await init_db()
    logger.info("Database initialized successfully")

    yield

    # Shutdown
    logger.info("Shutting down CV2Interview application")
    await close_db()
    logger.info("Database connections closed")

# Create FastAPI application
app = FastAPI(
    title="CV2Interview API",
    description="Advanced AI-powered CV analysis and interview preparation platform",
    version="2.0.0",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    lifespan=lifespan
)

# Security and middleware will be added when dependencies are installed

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if DEBUG else [
        "https://cv2interview.com",
        "https://www.cv2interview.com",
        "http://localhost:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing."""
    start_time = time.time()

    # Log request
    client_ip = request.client.host if request.client else "unknown"
    logger.info(
        f"Request started: {request.method} {request.url} from {client_ip}"
    )

    try:
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            process_time=round(process_time, 4),
        )

        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            "Request failed",
            method=request.method,
            url=str(request.url),
            error=str(e),
            process_time=round(process_time, 4),
        )
        raise

# Include routers
app.include_router(chat.router, prefix="/api/v1/agent", tags=["CV Analysis"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Analytics & Dashboard"])

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return JSONResponse(content={
        "status": "healthy",
        "environment": ENVIRONMENT,
        "version": "2.0.0",
        "timestamp": time.time()
    })

# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return JSONResponse(content={
        "message": "CV2Interview API v2.0",
        "description": "Advanced AI-powered CV analysis and interview preparation platform",
        "docs_url": "/docs" if DEBUG else "Documentation available in development mode",
        "version": "2.0.0",
        "features": [
            "Enhanced CV analysis with structured data extraction",
            "Advanced career recommendations with confidence scoring",
            "Intelligent interview question generation",
            "Comprehensive analytics and dashboards",
            "Real-time performance monitoring",
            "Rate limiting and security features"
        ]
    })

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(
        "Unhandled exception",
        method=request.method,
        url=str(request.url),
        error=str(exc),
        error_type=type(exc).__name__,
    )

    if DEBUG:
        # In debug mode, return detailed error information
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc),
                "type": type(exc).__name__,
                "debug": True
            }
        )
    else:
        # In production, return generic error message
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later.",
                "debug": False
            }
        )

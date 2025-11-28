"""
Main FastAPI application
Entry point for the NupatAI backend
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.api.v1 import auth, chats, messages
import time


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    NupatAI Backend API - Proudly Made in Africa for Africans 🌍
    
    An intelligent AI assistant powered by advanced language models.
    Built by Nupat Technologies.
    
    ## Features
    
    * **User Authentication** - Secure JWT-based authentication
    * **Chat Management** - Create and manage multiple chat sessions
    * **AI Responses** - Get intelligent responses powered by NupatAI
    * **Chat History** - Access complete conversation history
    * **Auto-Titling** - Automatic chat title generation
    
    ## Authentication
    
    Most endpoints require authentication. Include the JWT token in the Authorization header:
    
    ```
    Authorization: Bearer <your_access_token>
    ```
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add response time header to all responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed messages"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred",
            "error": str(exc) if settings.DEBUG else "Internal server error"
        }
    )


# Health check endpoint
@app.get("/", tags=["Health"])
def root():
    """
    Root endpoint - Health check
    
    Returns basic API information and status
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "message": "Welcome to NupatAI API - Proudly Made in Africa 🌍",
        "docs": "/docs",
        "tagline": "Intelligent. Fast. Helpful."
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Detailed health check endpoint
    
    Returns system health status
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION
    }


# Include API routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(chats.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup
    """
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"📝 Environment: {settings.ENVIRONMENT}")
    print(f"📚 API Documentation: /docs")
    print(f"🌍 Made in Africa for Africans by Nupat Technologies")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown
    """
    print(f"👋 {settings.APP_NAME} shutting down...")
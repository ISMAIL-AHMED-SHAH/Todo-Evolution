"""
FastAPI Main Application

Entry point for the Todo App backend API.
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
# Database session management is handled via dependency injection (get_session)
from src.middleware import AuthMiddleware
from src.middleware.error_handler import (
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler
)
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.api.users import router as users_router
from src.utils.logger import app_logger
from src.middleware.logging_middleware import LoggingMiddleware

# Load environment variables
load_dotenv()

logger = app_logger

# Initialize FastAPI app
app = FastAPI(
    title="Todo App API",
    description="Full-stack multi-user todo application with authentication",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """Initialize application on startup"""
    logger.info("Starting Todo App API...")
    # NOTE: Database tables are managed by Alembic migrations, not SQLModel.metadata.create_all()
    # Run migrations using: alembic upgrade head
    logger.info("Application startup complete")


# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include authentication routes
app.include_router(auth_router)

# Include task routes
app.include_router(tasks_router)

# Include user profile routes
app.include_router(users_router)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# CORS configuration (from environment or defaults)
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
origins = [origin.strip() for origin in cors_origins_env.split(",")]

logger.info(f"CORS enabled for origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(
        content={
            "message": "Todo App API",
            "version": "1.0.0",
            "status": "running"
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "todo-app-backend"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

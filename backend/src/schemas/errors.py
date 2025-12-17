"""
Error response models for consistent API error handling
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ErrorDetail(BaseModel):
    """
    Detailed error information for validation errors.
    """
    field: str = Field(..., description="Field name that caused the error")
    message: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ErrorResponse(BaseModel):
    """
    Standard error response model for all API errors.
    """
    error: str = Field(..., description="Error type or code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information (for validation errors)")
    status_code: int = Field(..., description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "type": "value_error.email"
                    }
                ],
                "status_code": 422
            }
        }


class NotFoundError(BaseModel):
    """
    Error response for resource not found (404).
    """
    error: str = Field(default="NotFound", description="Error type")
    message: str = Field(..., description="Resource not found message")
    resource: Optional[str] = Field(None, description="Resource type that was not found")
    status_code: int = Field(default=404, description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "NotFound",
                "message": "Task not found",
                "resource": "Task",
                "status_code": 404
            }
        }


class UnauthorizedError(BaseModel):
    """
    Error response for authentication failures (401).
    """
    error: str = Field(default="Unauthorized", description="Error type")
    message: str = Field(..., description="Authentication error message")
    status_code: int = Field(default=401, description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Unauthorized",
                "message": "Invalid or expired token",
                "status_code": 401
            }
        }


class ForbiddenError(BaseModel):
    """
    Error response for authorization failures (403).
    """
    error: str = Field(default="Forbidden", description="Error type")
    message: str = Field(..., description="Authorization error message")
    status_code: int = Field(default=403, description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Forbidden",
                "message": "You do not have permission to access this resource",
                "status_code": 403
            }
        }


class ConflictError(BaseModel):
    """
    Error response for resource conflicts (409).
    """
    error: str = Field(default="Conflict", description="Error type")
    message: str = Field(..., description="Conflict error message")
    resource: Optional[str] = Field(None, description="Resource type that conflicts")
    status_code: int = Field(default=409, description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Conflict",
                "message": "User with this email already exists",
                "resource": "User",
                "status_code": 409
            }
        }


class DatabaseError(BaseModel):
    """
    Error response for database errors (500).
    """
    error: str = Field(default="DatabaseError", description="Error type")
    message: str = Field(..., description="Database error message")
    status_code: int = Field(default=500, description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "DatabaseError",
                "message": "Database operation failed",
                "status_code": 500
            }
        }


class InternalServerError(BaseModel):
    """
    Error response for internal server errors (500).
    """
    error: str = Field(default="InternalServerError", description="Error type")
    message: str = Field(..., description="Error message")
    status_code: int = Field(default=500, description="HTTP status code")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "status_code": 500
            }
        }

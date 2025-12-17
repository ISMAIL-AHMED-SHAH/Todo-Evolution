"""
User profile API endpoints with Phase 2 enhancements
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any

from src.database import get_session
from src.models.user import User
from src.schemas.user import UserResponse, UserUpdate
from src.schemas.errors import NotFoundError, ForbiddenError, ConflictError
from src.auth.jwt_handler import jwt_bearer
from src.services.user_service import UserService


router = APIRouter(prefix="/api", tags=["Users"])


@router.get("/{user_id}/profile", response_model=UserResponse)
async def get_user_profile(
    user_id: int,
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> Any:
    """
    Get user profile information (T032).

    Returns:
    - User ID
    - Email
    - Created timestamp
    - Updated timestamp

    Security:
    - Requires valid JWT token
    - User can only access their own profile
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own profile"
        )

    # Get user from database
    user = UserService.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.put("/{user_id}/profile", response_model=UserResponse)
async def update_user_profile(
    user_id: int,
    user_update: UserUpdate,
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> Any:
    """
    Update user profile information (T033).

    Allows updating:
    - Email address (must be valid and unique)
    - Password (requires current password for verification)

    Security:
    - Requires valid JWT token
    - User can only update their own profile
    - Current password required for password changes
    - Email uniqueness validation

    Returns:
    - Updated user profile with 200 OK
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    # Validate email uniqueness if email is being changed
    if user_update.email:
        existing_user = UserService.get_user_by_email(session, user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email address already in use"
            )

    # Validate password change requirements
    if user_update.new_password and not user_update.current_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is required to set a new password"
        )

    # Update user using the service
    try:
        updated_user = UserService.update_user(session, user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except ValueError as e:
        # Handle incorrect current password error from service
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return UserResponse(
        id=updated_user.id,
        email=updated_user.email,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )

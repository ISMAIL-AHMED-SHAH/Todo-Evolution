"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Any
from datetime import timedelta
from pydantic import BaseModel, EmailStr

from src.database import get_session
from src.models.user import User, UserCreate
from src.auth import verify_password, get_password_hash, create_access_token, get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str


@router.post("/signup")
async def signup(user_create: UserCreate, session: Session = Depends(get_session)) -> Any:
    """
    User registration endpoint
    """
    import logging
    import traceback
    logger = logging.getLogger(__name__)

    try:
        # Check if user already exists
        logger.info(f"Checking for existing user with email: {user_create.email}")
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Hash the password
        logger.info("Hashing password")
        hashed_password = get_password_hash(user_create.password)

        # Create new user
        logger.info(f"Creating new user with email: {user_create.email}")
        db_user = User(
            email=user_create.email,
            password_hash=hashed_password
        )

        logger.info("Adding user to session")
        session.add(db_user)

        logger.info("Committing transaction")
        session.commit()

        logger.info("Refreshing user object")
        session.refresh(db_user)

        logger.info(f"User created successfully with ID: {db_user.id}")

        # Return user info without password
        return {
            "id": db_user.id,
            "email": db_user.email
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


@router.post("/signin")
async def signin(login_data: LoginRequest, session: Session = Depends(get_session)) -> Any:
    """
    User login endpoint
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == login_data.email)).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # 30 minutes expiry
    access_token = create_access_token(
        data={"sub": str(user.id)},  # Use string for sub as per JWT standard
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)) -> Any:
    """
    Get authenticated user's profile information
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)) -> Any:
    """
    Logout endpoint

    Note: Since we're using JWT tokens, the actual token invalidation happens client-side.
    This endpoint exists for logging purposes and future enhancements like token blacklisting.
    """
    # In a production system, you might want to:
    # 1. Log the logout event
    # 2. Add the token to a blacklist (if implementing token revocation)
    # 3. Update last_logout_at timestamp in user record

    return {
        "message": "Successfully logged out",
        "user_id": current_user.id
    }
"""
User service for business logic operations
"""
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext
from src.models.user import User, UserCreate, UserUpdate

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Service class for user-related business logic
    """

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password from database

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            User object or None if not found
        """
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()
        return user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Get a user by their email address.

        Args:
            session: Database session
            email: User email address

        Returns:
            User object or None if not found
        """
        user = session.exec(
            select(User).where(User.email == email)
        ).first()
        return user

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """
        Create a new user with hashed password.

        Args:
            session: Database session
            user_create: User creation data

        Returns:
            Created user object
        """
        # Hash the password
        hashed_password = UserService.get_password_hash(user_create.password)

        # Create user with hashed password
        db_user = User(
            email=user_create.email,
            password_hash=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(session: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """
        Update user profile (email and/or password).

        Args:
            session: Database session
            user_id: User ID
            user_update: User update data

        Returns:
            Updated user object or None if not found
        """
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()

        if not user:
            return None

        # Update email if provided
        if user_update.email:
            user.email = user_update.email

        # Update password if new password provided and current password verified
        if user_update.new_password and user_update.current_password:
            # Verify current password
            if not UserService.verify_password(user_update.current_password, user.password_hash):
                raise ValueError("Current password is incorrect")

            # Hash and set new password
            user.password_hash = UserService.get_password_hash(user_update.new_password)

        # Update timestamp
        from datetime import datetime
        user.updated_at = datetime.utcnow()

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            session: Database session
            email: User email
            password: Plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = UserService.get_user_by_email(session, email)
        if not user:
            return None

        if not UserService.verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def delete_user(session: Session, user_id: int) -> bool:
        """
        Delete a user account.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            True if deleted, False if not found
        """
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()

        if not user:
            return False

        session.delete(user)
        session.commit()
        return True

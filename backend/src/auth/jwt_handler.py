"""
JWT verification middleware for Better Auth integration
Uses PyJWT to verify tokens signed by Better Auth with shared secret
"""
import os
import jwt
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

# Better Auth shared secret (MUST match frontend)
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication for FastAPI.
    Verifies JWT tokens from Better Auth using shared secret.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Extract and verify JWT token from request.

        Returns:
            Dict containing decoded JWT payload with user information

        Raises:
            HTTPException: If token is invalid, expired, or missing
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme. Expected Bearer token."
                )

            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired token"
                )

            return payload
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization credentials"
            )

    def verify_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token using Better Auth shared secret.

        Args:
            token: JWT token string from Authorization header

        Returns:
            Decoded JWT payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                BETTER_AUTH_SECRET,
                algorithms=[JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid
            return None
        except Exception:
            # Any other error
            return None


def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode JWT token without validation (for debugging).

    Args:
        token: JWT token string

    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        return payload
    except Exception:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID as integer or None if not found
    """
    payload = decode_jwt(token)
    if payload:
        # Better Auth typically stores user ID in 'sub' (subject) claim
        # or 'userId' field depending on configuration
        user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')
        if user_id:
            try:
                return int(user_id)
            except (ValueError, TypeError):
                return None
    return None


# Global instance for dependency injection
jwt_bearer = JWTBearer()

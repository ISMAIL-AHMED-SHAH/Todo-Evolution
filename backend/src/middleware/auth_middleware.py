"""
Authentication middleware for JWT token validation
"""
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
import os


SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"


class AuthMiddleware:
    """
    Middleware to handle JWT authentication
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        # Add the auth helper functions to the request state
        request.state.get_current_user_id = self.get_current_user_id
        request.state.verify_token = self.verify_token

        return await self.app(scope, receive, send)

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def get_current_user_id(self, request: Request) -> Optional[int]:
        """Extract user ID from the authorization header"""
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        if not (authorization and scheme and credentials):
            return None

        if scheme.lower() != "bearer":
            return None

        payload = self.verify_token(credentials)
        if payload is None:
            return None

        user_id = payload.get("sub")
        return user_id if isinstance(user_id, int) else None
"""
JWT Utilities

Helper functions for JWT token generation and validation.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
import base64
import hmac
import hashlib


class JWTHelper:
    """Helper for JWT token operations."""

    def __init__(self, secret: Optional[str] = None):
        """
        Initialize JWT helper.

        Args:
            secret: Secret key for signing tokens (defaults to env var)
        """
        self.secret = secret or "BETTER_AUTH_SECRET_CHANGEME"

    def encode_payload(self, payload: Dict[str, Any]) -> str:
        """
        Encode a payload to base64url.

        Args:
            payload: Dictionary to encode

        Returns:
            Base64url encoded string
        """
        json_str = json.dumps(payload, separators=(',', ':'))
        return base64.urlsafe_b64encode(json_str.encode()).decode().rstrip('=')

    def decode_payload(self, encoded: str) -> Dict[str, Any]:
        """
        Decode a base64url payload.

        Args:
            encoded: Base64url encoded string

        Returns:
            Decoded dictionary
        """
        # Add padding if needed
        padding = 4 - (len(encoded) % 4)
        if padding != 4:
            encoded += '=' * padding

        decoded = base64.urlsafe_b64decode(encoded)
        return json.loads(decoded)

    def create_token(
        self,
        user_id: int,
        email: str,
        expires_in: int = 3600
    ) -> str:
        """
        Create a JWT token.

        Args:
            user_id: User ID
            email: User email
            expires_in: Token expiration in seconds (default 1 hour)

        Returns:
            JWT token string
        """
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }

        now = datetime.utcnow()
        payload = {
            "user_id": user_id,
            "email": email,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=expires_in)).timestamp())
        }

        header_encoded = self.encode_payload(header)
        payload_encoded = self.encode_payload(payload)

        message = f"{header_encoded}.{payload_encoded}"
        signature = self._sign(message)

        return f"{message}.{signature}"

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded payload if valid, None otherwise
        """
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None

            header_encoded, payload_encoded, signature = parts
            message = f"{header_encoded}.{payload_encoded}"

            # Verify signature
            expected_signature = self._sign(message)
            if signature != expected_signature:
                return None

            # Decode payload
            payload = self.decode_payload(payload_encoded)

            # Check expiration
            if payload.get("exp", 0) < datetime.utcnow().timestamp():
                return None

            return payload

        except Exception:
            return None

    def extract_user_id(self, token: str) -> Optional[int]:
        """
        Extract user ID from token.

        Args:
            token: JWT token string

        Returns:
            User ID if valid, None otherwise
        """
        payload = self.verify_token(token)
        return payload.get("user_id") if payload else None

    def _sign(self, message: str) -> str:
        """Create HMAC signature for message."""
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()

        return base64.urlsafe_b64encode(signature).decode().rstrip('=')

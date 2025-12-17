"""
Authentication Integration Skills

Skills for configuring and working with Better Auth and JWT authentication.
"""

from typing import Dict, Any, Optional
from ..tools import JWTHelper


class AuthSkills:
    """Skills for JWT and Better Auth integration."""

    def __init__(self):
        """Initialize authentication skills."""
        self.jwt_helper = JWTHelper()

    def configure_better_auth_jwt(self) -> Dict[str, str]:
        """
        Generate Better Auth configuration for JWT.

        Returns:
            Dictionary of config_file: code

        Example:
            >>> skills = AuthSkills()
            >>> config = skills.configure_better_auth_jwt()
        """
        return {
            "auth.config.ts": self._generate_better_auth_config(),
            ".env.example": self._generate_env_template(),
        }

    def jwt_verification_middleware(self) -> str:
        """
        Generate JWT verification middleware for FastAPI.

        Returns:
            Middleware code

        Example:
            >>> skills = AuthSkills()
            >>> middleware = skills.jwt_verification_middleware()
        """
        return '''"""
JWT Verification Middleware for FastAPI
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import os

from intelligence.tools import JWTHelper

security = HTTPBearer()
jwt_helper = JWTHelper(secret=os.getenv("BETTER_AUTH_SECRET"))


async def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Verify JWT token from Authorization header.

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    payload = jwt_helper.verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def get_current_user(
    payload: Dict[str, Any] = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    """
    Extract current user from JWT payload.

    Args:
        payload: Decoded JWT payload

    Returns:
        User information
    """
    return {
        "user_id": payload.get("user_id"),
        "email": payload.get("email"),
    }


async def verify_user_ownership(
    user_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> bool:
    """
    Verify that authenticated user owns the resource.

    Args:
        user_id: User ID from URL path
        current_user: Current authenticated user

    Returns:
        True if ownership verified

    Raises:
        HTTPException: If user doesn't own resource
    """
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    return True
'''

    def sync_frontend_backend_auth(self) -> Dict[str, str]:
        """
        Generate code to sync authentication between frontend and backend.

        Returns:
            Dictionary of component_name: code
        """
        return {
            "useAuth.ts": self._generate_use_auth_hook(),
            "AuthProvider.tsx": self._generate_auth_provider(),
        }

    def enforce_user_isolation(self) -> str:
        """
        Generate user isolation enforcement decorator.

        Returns:
            Python decorator code

        Example:
            >>> skills = AuthSkills()
            >>> decorator = skills.enforce_user_isolation()
        """
        return '''"""
User Isolation Enforcement Decorator
"""

from functools import wraps
from fastapi import HTTPException, status
from typing import Callable, Any


def enforce_user_isolation(func: Callable) -> Callable:
    """
    Decorator to enforce user isolation on endpoint handlers.

    Usage:
        @router.get("/api/{user_id}/tasks")
        @enforce_user_isolation
        async def get_tasks(user_id: int, current_user: dict = Depends(get_current_user)):
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract user_id from kwargs
        url_user_id = kwargs.get("user_id")
        current_user = kwargs.get("current_user", {})

        # Verify ownership
        if url_user_id != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: User isolation violation"
            )

        return await func(*args, **kwargs)

    return wrapper
'''

    def _generate_better_auth_config(self) -> str:
        """Generate Better Auth configuration file."""
        return '''/**
 * Better Auth Configuration
 */

import { betterAuth } from "better-auth";

export const auth = betterAuth({
    database: {
        provider: "postgresql",
        url: process.env.DATABASE_URL!,
    },
    emailAndPassword: {
        enabled: true,
        requireEmailVerification: false, // Set to true for production
    },
    session: {
        expiresIn: 60 * 60 * 24 * 7, // 7 days
        updateAge: 60 * 60 * 24, // 1 day
    },
    jwt: {
        secret: process.env.BETTER_AUTH_SECRET!,
        expiresIn: "7d",
    },
});

export type Session = typeof auth.$Infer.Session;
'''

    def _generate_env_template(self) -> str:
        """Generate environment variable template."""
        return '''# Authentication
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# API
NEXT_PUBLIC_API_URL=http://localhost:8000
'''

    def _generate_use_auth_hook(self) -> str:
        """Generate React hook for authentication."""
        return '''/**
 * useAuth Hook - Authentication State Management
 */

import { useState, useEffect, createContext, useContext } from "react";

interface User {
    user_id: number;
    email: string;
}

interface AuthContext {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    signin: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string) => Promise<void>;
    signout: () => Promise<void>;
}

const AuthContext = createContext<AuthContext | undefined>(undefined);

export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used within AuthProvider");
    }

    return context;
}

export { AuthContext };
'''

    def _generate_auth_provider(self) -> str:
        """Generate Auth Provider component."""
        return '''/**
 * Auth Provider - Global Authentication State
 */

"use client";

import { useState, useEffect, ReactNode } from "react";
import { AuthContext } from "./useAuth";
import { apiClient } from "../services/api-client";

interface AuthProviderProps {
    children: ReactNode;
}

export default function AuthProvider({ children }: AuthProviderProps) {
    const [user, setUser] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check for existing token on mount
        const token = localStorage.getItem("auth_token");

        if (token) {
            // TODO: Verify token and set user
            // For now, just mark as loaded
            setIsLoading(false);
        } else {
            setIsLoading(false);
        }
    }, []);

    const signin = async (email: string, password: string) => {
        const result = await apiClient.signin(email, password);
        // TODO: Decode token and set user
        setUser({ email });
    };

    const signup = async (email: string, password: string) => {
        const result = await apiClient.signup(email, password);
        // TODO: Decode token and set user
        setUser({ email });
    };

    const signout = async () => {
        await apiClient.signout();
        setUser(null);
    };

    const value = {
        user,
        isAuthenticated: !!user,
        isLoading,
        signin,
        signup,
        signout,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
'''

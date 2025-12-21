/**
 * useAuth Hook
 *
 * Custom React hook for authentication management with FastAPI backend.
 * Provides authentication state, login, logout, and session management.
 */

'use client';

import { useCallback, useEffect, useState } from 'react';
import type { User, LoginCredentials, RegisterInput } from '@/types/user';

/**
 * Authentication State Interface
 */
interface UseAuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/**
 * Authentication Actions Interface
 */
interface UseAuthActions {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (input: RegisterInput) => Promise<void>;
  logout: () => Promise<void>;
  refreshSession: () => Promise<void>;
  clearError: () => void;
}

/**
 * Complete useAuth Return Type
 */
export interface UseAuthReturn extends UseAuthState, UseAuthActions {}

/**
 * useAuth Hook
 *
 * Manages authentication state and provides methods for login, logout, and registration.
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isAuthenticated, login, logout } = useAuth();
 *
 *   const handleLogin = async () => {
 *     await login({ email: 'user@example.com', password: 'password' });
 *   };
 *
 *   if (!isAuthenticated) {
 *     return <LoginForm onSubmit={handleLogin} />;
 *   }
 *
 *   return <div>Welcome, {user?.email}!</div>;
 * }
 * ```
 */
export function useAuth(): UseAuthReturn {
  const [state, setState] = useState<UseAuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  /**
   * Load session on mount and check authentication status
   */
  const loadSession = useCallback(async () => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      // Get token from localStorage
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

      if (!token) {
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
        return;
      }

      // Call backend /auth/profile endpoint with token
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        // Token is invalid or expired
        if (typeof window !== 'undefined') {
          localStorage.removeItem('auth_token');
        }
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
        return;
      }

      const userData = await response.json();

      // Map backend user to our User type
      const user: User = {
        id: userData.id,
        email: userData.email,
        created_at: userData.created_at,
        updated_at: userData.updated_at,
      };

      setState({
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      console.error('Failed to load session:', error);
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to load session',
      });
    }
  }, []);

  /**
   * Login with email and password
   */
  const login = useCallback(async (credentials: LoginCredentials) => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      // Call backend /auth/signin endpoint
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      const data = await response.json();

      // Store token in localStorage for API client
      if (data.access_token && typeof window !== 'undefined') {
        localStorage.setItem('auth_token', data.access_token);
      }

      // Reload session to update state
      await loadSession();
    } catch (error) {
      console.error('Login error:', error);
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Login failed',
      }));
      throw error;
    }
  }, [loadSession]);

  /**
   * Register new user account
   */
  const register = useCallback(async (input: RegisterInput) => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      // Call backend /auth/signup endpoint
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: input.email,
          password: input.password,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }

      const userData = await response.json();

      // After signup, automatically log in to get token
      const loginResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: input.email,
          password: input.password,
        }),
      });

      if (loginResponse.ok) {
        const data = await loginResponse.json();
        if (data.access_token && typeof window !== 'undefined') {
          localStorage.setItem('auth_token', data.access_token);
        }
      }

      // Reload session to update state
      await loadSession();
    } catch (error) {
      console.error('Registration error:', error);
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Registration failed',
      }));
      throw error;
    }
  }, [loadSession]);

  /**
   * Logout current user
   */
  const logout = useCallback(async () => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      // Get token and call backend logout endpoint
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

      if (token) {
        try {
          await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/logout`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
        } catch (err) {
          // Continue with logout even if backend call fails
          console.warn('Backend logout failed:', err);
        }
      }

      // Clear token from localStorage
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
      }

      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      console.error('Logout error:', error);
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Logout failed',
      }));
      throw error;
    }
  }, []);

  /**
   * Refresh the current session
   */
  const refreshSession = useCallback(async () => {
    await loadSession();
  }, [loadSession]);

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  /**
   * Load session on mount
   */
  useEffect(() => {
    loadSession();
  }, [loadSession]);

  /**
   * Setup session refresh interval (every 5 minutes)
   */
  useEffect(() => {
    if (!state.isAuthenticated) return;

    const refreshInterval = setInterval(() => {
      loadSession();
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(refreshInterval);
  }, [state.isAuthenticated, loadSession]);

  return {
    // State
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    error: state.error,

    // Actions
    login,
    register,
    logout,
    refreshSession,
    clearError,
  };
}

/**
 * Hook to get the current user
 * Throws an error if not authenticated
 */
export function useRequireAuth(): User {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    throw new Error('Authentication is loading');
  }

  if (!isAuthenticated || !user) {
    throw new Error('User is not authenticated');
  }

  return user;
}

/**
 * Hook to get the user ID
 * Returns stable userId across page navigations by caching in localStorage
 * Returns null only when explicitly not authenticated
 */
export function useUserId(): number | null {
  const { user, isAuthenticated, isLoading } = useAuth();

  // If authenticated and user exists, cache and return userId
  if (isAuthenticated && user) {
    if (typeof window !== 'undefined') {
      localStorage.setItem('cached_user_id', String(user.id));
    }
    return user.id;
  }

  // If still loading, return cached userId to prevent cache key changes
  if (isLoading) {
    if (typeof window !== 'undefined') {
      const cachedId = localStorage.getItem('cached_user_id');
      if (cachedId) {
        return parseInt(cachedId, 10);
      }
    }
  }

  // Only return null when explicitly not authenticated
  // Clear cached userId on logout
  if (!isAuthenticated && !isLoading) {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('cached_user_id');
    }
  }

  return null;
}

/**
 * Hook to check authentication status
 * Useful for conditional rendering
 */
export function useIsAuthenticated(): boolean {
  const { isAuthenticated } = useAuth();
  return isAuthenticated;
}

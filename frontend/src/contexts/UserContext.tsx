/**
 * User Context Provider for authentication state management
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { User, apiService } from '../services/api';

interface UserState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface UserContextType extends UserState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signup: (email: string, password: string) => Promise<void>;
  refreshUser: () => Promise<void>;
}

// Define action types
type UserAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'LOGIN_FAILURE' }
  | { type: 'SIGNUP_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'SIGNUP_FAILURE' }
  | { type: 'LOGOUT' }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_USER'; payload: User };

// Initial state
const initialState: UserState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
};

// Reducer function
const userReducer = (state: UserState, action: UserAction): UserState => {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        isLoading: true,
      };
    case 'LOGIN_SUCCESS':
      localStorage.setItem('auth_token', action.payload.token);
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
      };
    case 'LOGIN_FAILURE':
      localStorage.removeItem('auth_token');
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      };
    case 'SIGNUP_SUCCESS':
      localStorage.setItem('auth_token', action.payload.token);
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
      };
    case 'SIGNUP_FAILURE':
      localStorage.removeItem('auth_token');
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      };
    case 'LOGOUT':
      localStorage.removeItem('auth_token');
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
      };
    default:
      return state;
  }
};

// Create context
const UserContext = createContext<UserContextType | undefined>(undefined);

// Provider component
export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(userReducer, initialState);

  // Check for existing token on initial load
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      // Token exists, try to refresh user info
      refreshUser();
    } else {
      // No token, set loading to false
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, []);

  // Function to refresh user data
  const refreshUser = async () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        dispatch({ type: 'SET_LOADING', payload: true });
        const user = await apiService.getProfile();
        dispatch({ type: 'SET_USER', payload: user });
      } catch (error) {
        console.error('Failed to refresh user:', error);
        localStorage.removeItem('auth_token');
        dispatch({ type: 'LOGOUT' });
      }
    } else {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  // Login function
  const login = async (email: string, password: string) => {
    try {
      dispatch({ type: 'LOGIN_START' });
      const response = await apiService.signin(email, password);
      const token = response.access_token;

      // Get user profile after successful login
      const user = await apiService.getProfile();

      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: { user, token }
      });
    } catch (error) {
      console.error('Login failed:', error);
      dispatch({ type: 'LOGIN_FAILURE' });
      throw error;
    }
  };

  // Signup function
  const signup = async (email: string, password: string) => {
    try {
      dispatch({ type: 'LOGIN_START' });
      const user = await apiService.signup(email, password);

      // After signup, user is typically automatically logged in
      // For this implementation, we'll treat signup like login
      // In a real app, this might require email verification
      const response = await apiService.signin(email, password);
      const token = response.access_token;

      dispatch({
        type: 'SIGNUP_SUCCESS',
        payload: { user, token }
      });
    } catch (error) {
      console.error('Signup failed:', error);
      dispatch({ type: 'SIGNUP_FAILURE' });
      throw error;
    }
  };

  // Logout function
  const logout = async () => {
    try {
      // Call backend logout endpoint (optional - for logging/tracking)
      await apiService.logout();
    } catch (error) {
      // Continue with logout even if backend call fails
      console.error('Backend logout failed:', error);
    } finally {
      // Always clear local state and storage
      dispatch({ type: 'LOGOUT' });
    }
  };

  const value = {
    ...state,
    login,
    logout,
    signup,
    refreshUser,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

// Custom hook to use the user context
export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
/**
 * Custom hook for authentication
 * Provides authentication-related functionality
 */

import { useUser } from '../contexts/UserContext';
import { apiService } from '../services/api';

export const useAuth = () => {
  const { user, token, isAuthenticated, isLoading, login, logout, signup, refreshUser } = useUser();

  // Additional auth-related functions can be added here
  const checkAuthStatus = (): boolean => {
    return isAuthenticated && !!user;
  };

  const getToken = (): string | null => {
    return token;
  };

  const getCurrentUser = () => {
    return user;
  };

  // Function to update task completion status
  const updateTaskCompletion = async (userId: number, taskId: number, completed: boolean) => {
    if (!isAuthenticated) {
      throw new Error('User not authenticated');
    }
    return apiService.updateTaskCompletion(userId, taskId, completed);
  };

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    login,
    logout,
    signup,
    refreshUser,
    checkAuthStatus,
    getToken,
    getCurrentUser,
    updateTaskCompletion,
  };
};
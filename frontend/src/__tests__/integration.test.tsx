/**
 * Integration tests for frontend-backend communication
 *
 * Tests the complete flow from UI actions to database persistence
 * including authentication, task CRUD operations, and error handling
 */

import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '../hooks/useAuth';
import { useTasks } from '../hooks/useTasks';
import { UserProvider } from '../contexts/UserContext';
import { apiService } from '../services/api';

// Mock the API service
jest.mock('../services/api', () => ({
  apiService: {
    signin: jest.fn(),
    signup: jest.fn(),
    getProfile: jest.fn(),
    getTasks: jest.fn(),
    createTask: jest.fn(),
    updateTask: jest.fn(),
    deleteTask: jest.fn(),
    updateTaskCompletion: jest.fn(),
  },
}));

const mockApiService = apiService as jest.Mocked<typeof apiService>;

// Wrapper component for hooks that need UserProvider
const wrapper = ({ children }: { children: React.ReactNode }) => (
  <UserProvider>{children}</UserProvider>
);

describe('Frontend-Backend Integration', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    // Clear localStorage
    localStorage.clear();
  });

  describe('Authentication Flow', () => {
    it('should sign in user and fetch profile', async () => {
      const mockUser = {
        id: 1,
        email: 'test@example.com',
        created_at: '2025-12-10T00:00:00Z',
        updated_at: '2025-12-10T00:00:00Z',
      };

      mockApiService.signin.mockResolvedValue({
        access_token: 'test-token',
        token_type: 'bearer',
      });
      mockApiService.getProfile.mockResolvedValue(mockUser);

      const { result } = renderHook(() => useAuth(), { wrapper });

      // Wait for initial loading to complete
      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Sign in
      await result.current.login('test@example.com', 'password');

      // Verify user is authenticated
      await waitFor(() => {
        expect(result.current.isAuthenticated).toBe(true);
        expect(result.current.user).toEqual(mockUser);
        expect(result.current.token).toBe('test-token');
      });

      // Verify API calls
      expect(mockApiService.signin).toHaveBeenCalledWith('test@example.com', 'password');
      expect(mockApiService.getProfile).toHaveBeenCalled();

      // Verify token is stored in localStorage
      expect(localStorage.getItem('auth_token')).toBe('test-token');
    });

    it('should handle sign in errors', async () => {
      mockApiService.signin.mockRejectedValue(new Error('Invalid credentials'));

      const { result } = renderHook(() => useAuth(), { wrapper });

      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Attempt sign in
      await expect(
        result.current.login('test@example.com', 'wrong-password')
      ).rejects.toThrow('Invalid credentials');

      // Verify user is not authenticated
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.user).toBeNull();
    });

    it('should sign out user', async () => {
      const mockUser = {
        id: 1,
        email: 'test@example.com',
        created_at: '2025-12-10T00:00:00Z',
        updated_at: '2025-12-10T00:00:00Z',
      };

      mockApiService.signin.mockResolvedValue({
        access_token: 'test-token',
        token_type: 'bearer',
      });
      mockApiService.getProfile.mockResolvedValue(mockUser);

      const { result } = renderHook(() => useAuth(), { wrapper });

      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Sign in
      await result.current.login('test@example.com', 'password');

      await waitFor(() => expect(result.current.isAuthenticated).toBe(true));

      // Sign out
      result.current.logout();

      // Verify user is signed out
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(localStorage.getItem('auth_token')).toBeNull();
    });
  });

  describe('Task Management Flow', () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      created_at: '2025-12-10T00:00:00Z',
      updated_at: '2025-12-10T00:00:00Z',
    };

    const mockTasks = [
      {
        id: 1,
        user_id: 1,
        title: 'Task 1',
        description: 'Description 1',
        completed: false,
        created_at: '2025-12-10T00:00:00Z',
        updated_at: '2025-12-10T00:00:00Z',
      },
      {
        id: 2,
        user_id: 1,
        title: 'Task 2',
        description: 'Description 2',
        completed: true,
        created_at: '2025-12-10T00:00:00Z',
        updated_at: '2025-12-10T00:00:00Z',
      },
    ];

    beforeEach(() => {
      mockApiService.signin.mockResolvedValue({
        access_token: 'test-token',
        token_type: 'bearer',
      });
      mockApiService.getProfile.mockResolvedValue(mockUser);
      mockApiService.getTasks.mockResolvedValue(mockTasks);
    });

    it('should fetch tasks after authentication', async () => {
      const { result } = renderHook(() => useTasks(), { wrapper });

      // Wait for tasks to be fetched
      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(2);
        expect(result.current.isLoading).toBe(false);
      });

      // Verify tasks are loaded
      expect(result.current.tasks).toEqual(mockTasks);
      expect(mockApiService.getTasks).toHaveBeenCalledWith(mockUser.id);
    });

    it('should create a new task', async () => {
      const newTask = {
        id: 3,
        user_id: 1,
        title: 'New Task',
        description: 'New Description',
        completed: false,
        created_at: '2025-12-10T00:00:00Z',
        updated_at: '2025-12-10T00:00:00Z',
      };

      mockApiService.createTask.mockResolvedValue(newTask);

      const { result } = renderHook(() => useTasks(), { wrapper });

      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Create task
      await result.current.createTask({
        title: 'New Task',
        description: 'New Description',
      });

      // Verify task was created
      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(3);
        expect(result.current.tasks[2]).toEqual(newTask);
      });

      expect(mockApiService.createTask).toHaveBeenCalledWith(mockUser.id, {
        title: 'New Task',
        description: 'New Description',
      });
    });

    it('should update an existing task', async () => {
      const updatedTask = {
        ...mockTasks[0],
        title: 'Updated Task',
        description: 'Updated Description',
      };

      mockApiService.updateTask.mockResolvedValue(updatedTask);

      const { result } = renderHook(() => useTasks(), { wrapper });

      await waitFor(() => expect(result.current.tasks).toHaveLength(2));

      // Update task
      await result.current.updateTask(1, {
        title: 'Updated Task',
        description: 'Updated Description',
      });

      // Verify task was updated
      await waitFor(() => {
        const task = result.current.tasks.find(t => t.id === 1);
        expect(task?.title).toBe('Updated Task');
        expect(task?.description).toBe('Updated Description');
      });

      expect(mockApiService.updateTask).toHaveBeenCalledWith(mockUser.id, 1, {
        title: 'Updated Task',
        description: 'Updated Description',
      });
    });

    it('should delete a task', async () => {
      mockApiService.deleteTask.mockResolvedValue(mockTasks[0]);

      const { result } = renderHook(() => useTasks(), { wrapper });

      await waitFor(() => expect(result.current.tasks).toHaveLength(2));

      // Delete task
      await result.current.deleteTask(1);

      // Verify task was deleted
      await waitFor(() => {
        expect(result.current.tasks).toHaveLength(1);
        expect(result.current.tasks.find(t => t.id === 1)).toBeUndefined();
      });

      expect(mockApiService.deleteTask).toHaveBeenCalledWith(mockUser.id, 1);
    });

    it('should toggle task completion', async () => {
      const toggledTask = {
        ...mockTasks[0],
        completed: true,
      };

      mockApiService.updateTaskCompletion.mockResolvedValue(toggledTask);

      const { result } = renderHook(() => useTasks(), { wrapper });

      await waitFor(() => expect(result.current.tasks).toHaveLength(2));

      // Toggle task completion
      await result.current.toggleTaskCompletion(1);

      // Verify task completion was toggled
      await waitFor(() => {
        const task = result.current.tasks.find(t => t.id === 1);
        expect(task?.completed).toBe(true);
      });

      expect(mockApiService.updateTaskCompletion).toHaveBeenCalledWith(mockUser.id, 1, true);
    });

    it('should handle task operation errors', async () => {
      mockApiService.createTask.mockRejectedValue(new Error('Failed to create task'));

      const { result } = renderHook(() => useTasks(), { wrapper });

      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Attempt to create task
      await expect(
        result.current.createTask({ title: 'New Task' })
      ).rejects.toThrow('Failed to create task');

      // Verify error is set
      expect(result.current.error).toBe('Failed to create task');
    });
  });

  describe('Error Handling', () => {
    it('should handle network errors gracefully', async () => {
      mockApiService.signin.mockRejectedValue(new Error('Network error'));

      const { result } = renderHook(() => useAuth(), { wrapper });

      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Attempt operation
      await expect(
        result.current.login('test@example.com', 'password')
      ).rejects.toThrow('Network error');
    });

    it('should clear errors when requested', async () => {
      mockApiService.getTasks.mockRejectedValue(new Error('Failed to fetch'));

      const { result } = renderHook(() => useTasks(), { wrapper });

      await waitFor(() => expect(result.current.error).not.toBeNull());

      // Clear error
      result.current.clearError();

      // Verify error is cleared
      expect(result.current.error).toBeNull();
    });
  });

  describe('Complete User Flow', () => {
    it('should handle complete user workflow: signup -> create task -> update -> delete', async () => {
      const mockUser = {
        id: 1,
        email: 'newuser@example.com',
        created_at: '2025-12-10T00:00:00Z',
        updated_at: '2025-12-10T00:00:00Z',
      };

      const mockTask = {
        id: 1,
        user_id: 1,
        title: 'First Task',
        description: 'My first task',
        completed: false,
        created_at: '2025-12-10T00:00:00Z',
        updated_at: '2025-12-10T00:00:00Z',
      };

      // Mock API responses
      mockApiService.signup.mockResolvedValue(mockUser);
      mockApiService.signin.mockResolvedValue({
        access_token: 'new-token',
        token_type: 'bearer',
      });
      mockApiService.getProfile.mockResolvedValue(mockUser);
      mockApiService.getTasks.mockResolvedValue([]);
      mockApiService.createTask.mockResolvedValue(mockTask);
      mockApiService.updateTask.mockResolvedValue({
        ...mockTask,
        title: 'Updated Task',
      });
      mockApiService.deleteTask.mockResolvedValue(mockTask);

      const { result: authResult } = renderHook(() => useAuth(), { wrapper });
      const { result: tasksResult } = renderHook(() => useTasks(), { wrapper });

      // Step 1: Signup
      await authResult.current.signup('newuser@example.com', 'password');
      await waitFor(() => expect(authResult.current.isAuthenticated).toBe(true));

      // Step 2: Create task
      await tasksResult.current.createTask({
        title: 'First Task',
        description: 'My first task',
      });
      await waitFor(() => expect(tasksResult.current.tasks).toHaveLength(1));

      // Step 3: Update task
      await tasksResult.current.updateTask(1, { title: 'Updated Task' });
      await waitFor(() => {
        expect(tasksResult.current.tasks[0].title).toBe('Updated Task');
      });

      // Step 4: Delete task
      await tasksResult.current.deleteTask(1);
      await waitFor(() => expect(tasksResult.current.tasks).toHaveLength(0));

      // Verify all API calls were made
      expect(mockApiService.signup).toHaveBeenCalled();
      expect(mockApiService.signin).toHaveBeenCalled();
      expect(mockApiService.createTask).toHaveBeenCalled();
      expect(mockApiService.updateTask).toHaveBeenCalled();
      expect(mockApiService.deleteTask).toHaveBeenCalled();
    });
  });
});

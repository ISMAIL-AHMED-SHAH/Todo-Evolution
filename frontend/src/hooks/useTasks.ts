/**
 * useTasks hook for task management
 *
 * Provides task CRUD operations with loading states, error handling,
 * and optimistic updates
 */

import { useState, useCallback, useEffect } from 'react';
import { apiService, Task, TaskCreate, TaskUpdate } from '../services/api';
import { useAuth } from './useAuth';

interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  fetchTasks: () => Promise<void>;
  createTask: (taskData: TaskCreate) => Promise<Task>;
  updateTask: (taskId: number, taskData: TaskUpdate) => Promise<Task>;
  deleteTask: (taskId: number) => Promise<void>;
  toggleTaskCompletion: (taskId: number) => Promise<Task>;
  clearError: () => void;
}

export function useTasks(): UseTasksReturn {
  const { user, isAuthenticated } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch all tasks for the current user
  const fetchTasks = useCallback(async () => {
    if (!isAuthenticated || !user) {
      setTasks([]);
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const fetchedTasks = await apiService.getTasks(user.id);
      setTasks(fetchedTasks);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch tasks';
      setError(errorMessage);
      console.error('Error fetching tasks:', err);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated, user]);

  // Create a new task
  const createTask = useCallback(async (taskData: TaskCreate): Promise<Task> => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    setIsLoading(true);
    setError(null);
    try {
      const newTask = await apiService.createTask(user.id, taskData);
      // Optimistically add to local state
      setTasks(prev => [...prev, newTask]);
      return newTask;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create task';
      setError(errorMessage);
      console.error('Error creating task:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  // Update an existing task
  const updateTask = useCallback(async (taskId: number, taskData: TaskUpdate): Promise<Task> => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    setIsLoading(true);
    setError(null);
    try {
      const updatedTask = await apiService.updateTask(user.id, taskId, taskData);
      // Update local state
      setTasks(prev =>
        prev.map(task => (task.id === taskId ? updatedTask : task))
      );
      return updatedTask;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setError(errorMessage);
      console.error('Error updating task:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  // Delete a task
  const deleteTask = useCallback(async (taskId: number): Promise<void> => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    setIsLoading(true);
    setError(null);
    try {
      await apiService.deleteTask(user.id, taskId);
      // Remove from local state
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete task';
      setError(errorMessage);
      console.error('Error deleting task:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  // Toggle task completion status
  const toggleTaskCompletion = useCallback(async (taskId: number): Promise<Task> => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    const task = tasks.find(t => t.id === taskId);
    if (!task) {
      throw new Error('Task not found');
    }

    // Optimistic update
    const optimisticTasks = tasks.map(t =>
      t.id === taskId ? { ...t, completed: !t.completed } : t
    );
    setTasks(optimisticTasks);

    setError(null);
    try {
      const updatedTask = await apiService.updateTaskCompletion(
        user.id,
        taskId,
        !task.completed
      );
      // Update with server response
      setTasks(prev =>
        prev.map(t => (t.id === taskId ? updatedTask : t))
      );
      return updatedTask;
    } catch (err) {
      // Revert optimistic update on error
      setTasks(tasks);
      const errorMessage = err instanceof Error ? err.message : 'Failed to toggle task completion';
      setError(errorMessage);
      console.error('Error toggling task completion:', err);
      throw err;
    }
  }, [user, tasks]);

  // Clear error state
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Fetch tasks when user changes
  useEffect(() => {
    if (isAuthenticated && user) {
      fetchTasks();
    }
  }, [isAuthenticated, user, fetchTasks]);

  return {
    tasks,
    isLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    clearError,
  };
}

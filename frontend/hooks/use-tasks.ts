/**
 * useTasks Hook
 *
 * Custom React Query hook for fetching and managing tasks.
 * Provides automatic caching, refetching, and loading states.
 */

'use client';

import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import type { Task, TaskFilterParams, TaskListResponse } from '@/types/task';
import type { ApiErrorResponse } from '@/types/api';

/**
 * Query Keys for React Query Cache
 */
export const taskQueryKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskQueryKeys.all, 'list'] as const,
  list: (userId: number, filters?: TaskFilterParams) =>
    [...taskQueryKeys.lists(), userId, filters] as const,
  details: () => [...taskQueryKeys.all, 'detail'] as const,
  detail: (userId: number, taskId: number) => [...taskQueryKeys.details(), userId, taskId] as const,
  stats: (userId: number) => [...taskQueryKeys.all, 'stats', userId] as const,
};

/**
 * Fetch tasks from the API
 */
async function fetchTasks(userId: number, filters?: TaskFilterParams): Promise<Task[]> {
  // Build query parameters
  const params: Record<string, string | number | boolean> = {};

  if (filters?.completed !== undefined) {
    params.completed = filters.completed;
  }
  if (filters?.priority) {
    params.priority = filters.priority;
  }
  if (filters?.overdue !== undefined) {
    params.overdue = filters.overdue;
  }
  if (filters?.category) {
    params.category = filters.category;
  }
  if (filters?.sortBy) {
    params.sort_by = filters.sortBy;
  }
  if (filters?.sortOrder) {
    params.sort_order = filters.sortOrder;
  }

  // Build URL with query parameters
  const queryString = new URLSearchParams(
    Object.entries(params).map(([key, value]) => [key, String(value)])
  ).toString();

  const endpoint = `/api/${userId}/tasks${queryString ? `?${queryString}` : ''}`;

  // Fetch tasks from API
  const response = await apiClient.get<TaskListResponse>(endpoint);

  // Handle different response formats
  if (Array.isArray(response)) {
    return response as unknown as Task[];
  }

  if (response && typeof response === 'object' && 'tasks' in response) {
    return (response as TaskListResponse).tasks;
  }

  // Fallback: return empty array
  return [];
}

/**
 * Fetch a single task by ID
 */
async function fetchTaskById(userId: number, taskId: number): Promise<Task> {
  const endpoint = `/api/${userId}/tasks/${taskId}`;
  const response = await apiClient.get<Task | { task: Task }>(endpoint);

  // Handle different response formats
  if (response && typeof response === 'object' && 'task' in response) {
    return response.task;
  }

  return response as Task;
}

/**
 * useTasks Hook
 *
 * Fetches and caches a list of tasks for a user with optional filtering.
 *
 * @param userId - The ID of the user whose tasks to fetch
 * @param filters - Optional filters to apply to the task list
 * @param options - React Query options
 *
 * @example
 * ```tsx
 * function TaskList() {
 *   const userId = useUserId();
 *   const { data: tasks, isLoading, error } = useTasks(userId, {
 *     completed: false,
 *     priority: 'High',
 *   });
 *
 *   if (isLoading) return <Spinner />;
 *   if (error) return <ErrorMessage error={error} />;
 *
 *   return (
 *     <ul>
 *       {tasks?.map((task) => (
 *         <li key={task.id}>{task.title}</li>
 *       ))}
 *     </ul>
 *   );
 * }
 * ```
 */
export function useTasks(
  userId: number | null,
  filters?: TaskFilterParams,
  options?: {
    enabled?: boolean;
    staleTime?: number;
    refetchInterval?: number;
  }
): UseQueryResult<Task[], ApiErrorResponse> {
  return useQuery<Task[], ApiErrorResponse>({
    queryKey: taskQueryKeys.list(userId ?? 0, filters),
    queryFn: () => {
      if (!userId) {
        throw new Error('User ID is required');
      }
      return fetchTasks(userId, filters);
    },
    enabled: !!userId && (options?.enabled ?? true),
    staleTime: options?.staleTime ?? 5 * 60 * 1000, // 5 minutes default
    refetchInterval: options?.refetchInterval,
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}

/**
 * useTask Hook
 *
 * Fetches and caches a single task by ID.
 *
 * @param userId - The ID of the user who owns the task
 * @param taskId - The ID of the task to fetch
 * @param options - React Query options
 *
 * @example
 * ```tsx
 * function TaskDetail({ taskId }: { taskId: number }) {
 *   const userId = useUserId();
 *   const { data: task, isLoading, error } = useTask(userId, taskId);
 *
 *   if (isLoading) return <Spinner />;
 *   if (error) return <ErrorMessage error={error} />;
 *   if (!task) return <NotFound />;
 *
 *   return <TaskCard task={task} />;
 * }
 * ```
 */
export function useTask(
  userId: number | null,
  taskId: number | null,
  options?: {
    enabled?: boolean;
    staleTime?: number;
  }
): UseQueryResult<Task, ApiErrorResponse> {
  return useQuery<Task, ApiErrorResponse>({
    queryKey: taskQueryKeys.detail(userId ?? 0, taskId ?? 0),
    queryFn: () => {
      if (!userId || !taskId) {
        throw new Error('User ID and Task ID are required');
      }
      return fetchTaskById(userId, taskId);
    },
    enabled: !!userId && !!taskId && (options?.enabled ?? true),
    staleTime: options?.staleTime ?? 5 * 60 * 1000, // 5 minutes default
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}

/**
 * useAllTasks Hook
 *
 * Fetches all tasks without filters (convenience wrapper).
 *
 * @param userId - The ID of the user whose tasks to fetch
 */
export function useAllTasks(userId: number | null): UseQueryResult<Task[], ApiErrorResponse> {
  return useTasks(userId);
}

/**
 * useCompletedTasks Hook
 *
 * Fetches only completed tasks (convenience wrapper).
 *
 * @param userId - The ID of the user whose tasks to fetch
 */
export function useCompletedTasks(userId: number | null): UseQueryResult<Task[], ApiErrorResponse> {
  return useTasks(userId, { completed: true });
}

/**
 * usePendingTasks Hook
 *
 * Fetches only pending (incomplete) tasks (convenience wrapper).
 *
 * @param userId - The ID of the user whose tasks to fetch
 */
export function usePendingTasks(userId: number | null): UseQueryResult<Task[], ApiErrorResponse> {
  return useTasks(userId, { completed: false });
}

/**
 * useOverdueTasks Hook
 *
 * Fetches only overdue tasks (convenience wrapper).
 *
 * @param userId - The ID of the user whose tasks to fetch
 */
export function useOverdueTasks(userId: number | null): UseQueryResult<Task[], ApiErrorResponse> {
  return useTasks(userId, { overdue: true });
}

/**
 * useHighPriorityTasks Hook
 *
 * Fetches only high-priority tasks (convenience wrapper).
 *
 * @param userId - The ID of the user whose tasks to fetch
 */
export function useHighPriorityTasks(userId: number | null): UseQueryResult<Task[], ApiErrorResponse> {
  return useTasks(userId, { priority: 'High' });
}

/**
 * useTasksByCategory Hook
 *
 * Fetches tasks filtered by category (convenience wrapper).
 *
 * @param userId - The ID of the user whose tasks to fetch
 * @param category - The category to filter by
 */
export function useTasksByCategory(
  userId: number | null,
  category: string
): UseQueryResult<Task[], ApiErrorResponse> {
  return useTasks(userId, { category });
}

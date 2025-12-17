/**
 * useTaskMutations Hook
 *
 * Custom React Query hook for task mutations (create, update, delete, complete).
 * Provides optimistic updates, automatic cache invalidation, and error rollback.
 */

'use client';

import { useMutation, useQueryClient, UseMutationResult } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { taskQueryKeys } from './use-tasks';
import type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  TaskWithUIState,
} from '@/types/task';
import type { ApiErrorResponse } from '@/types/api';

/**
 * Create Task Mutation
 */
async function createTask(userId: number, input: CreateTaskInput): Promise<Task> {
  const endpoint = `/api/${userId}/tasks`;
  const response = await apiClient.post<Task | { task: Task }>(endpoint, input);

  // Handle different response formats
  if (response && typeof response === 'object' && 'task' in response) {
    return response.task;
  }

  return response as Task;
}

/**
 * Update Task Mutation
 */
async function updateTask(
  userId: number,
  taskId: number,
  input: UpdateTaskInput
): Promise<Task> {
  const endpoint = `/api/${userId}/tasks/${taskId}`;
  const response = await apiClient.put<Task | { task: Task }>(endpoint, input);

  // Handle different response formats
  if (response && typeof response === 'object' && 'task' in response) {
    return response.task;
  }

  return response as Task;
}

/**
 * Delete Task Mutation
 */
async function deleteTask(userId: number, taskId: number): Promise<void> {
  const endpoint = `/api/${userId}/tasks/${taskId}`;
  await apiClient.delete<void>(endpoint);
}

/**
 * Complete/Toggle Task Mutation
 */
async function toggleTaskCompletion(
  userId: number,
  taskId: number,
  completed: boolean
): Promise<Task> {
  const endpoint = `/api/${userId}/tasks/${taskId}/complete`;
  const response = await apiClient.patch<Task | { task: Task }>(endpoint, { completed });

  // Handle different response formats
  if (response && typeof response === 'object' && 'task' in response) {
    return response.task;
  }

  return response as Task;
}

/**
 * useTaskMutations Hook
 *
 * Provides mutation functions for all task operations with optimistic updates.
 *
 * @param userId - The ID of the user performing mutations
 * @param options - Optional callbacks for success/error handling
 *
 * @example
 * ```tsx
 * function TaskList() {
 *   const userId = useUserId();
 *   const { createTaskMutation, updateTaskMutation, deleteTaskMutation } = useTaskMutations(userId);
 *
 *   const handleCreate = () => {
 *     createTaskMutation.mutate({
 *       title: "New Task",
 *       priority: "High",
 *     });
 *   };
 *
 *   return <button onClick={handleCreate}>Add Task</button>;
 * }
 * ```
 */
export function useTaskMutations(
  userId: number | null,
  options?: {
    onCreateSuccess?: (task: Task) => void;
    onUpdateSuccess?: (task: Task) => void;
    onDeleteSuccess?: (taskId: number) => void;
    onToggleSuccess?: (task: Task) => void;
    onError?: (error: ApiErrorResponse) => void;
  }
) {
  const queryClient = useQueryClient();

  /**
   * Create Task Mutation
   */
  const createTaskMutation: UseMutationResult<Task, ApiErrorResponse, CreateTaskInput> =
    useMutation<Task, ApiErrorResponse, CreateTaskInput, { previousTasks?: Task[] }>({
      mutationFn: (input: CreateTaskInput) => {
        if (!userId) {
          throw new Error('User ID is required');
        }
        return createTask(userId, input);
      },

      // Optimistic update: Add task to cache immediately
      onMutate: async (newTask) => {
        if (!userId) return {};

        // Cancel outgoing refetches
        await queryClient.cancelQueries({ queryKey: taskQueryKeys.lists() });

        // Snapshot previous value
        const previousTasks = queryClient.getQueryData<Task[]>(
          taskQueryKeys.list(userId)
        );

        // Optimistically update cache
        queryClient.setQueryData<Task[]>(taskQueryKeys.list(userId), (old = []) => {
          const optimisticTask: TaskWithUIState = {
            id: Date.now(), // Temporary ID
            user_id: userId,
            title: newTask.title,
            description: newTask.description || null,
            priority: newTask.priority || 'Medium',
            category: newTask.category || [],
            due_date: newTask.due_date || null,
            completed: false,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            _isOptimistic: true,
          };
          return [optimisticTask, ...old];
        });

        // Return context for rollback
        return { previousTasks };
      },

      // On error, rollback to previous state
      onError: (error, _newTask, context) => {
        if (context?.previousTasks && userId) {
          queryClient.setQueryData(taskQueryKeys.list(userId), context.previousTasks);
        }
        options?.onError?.(error);
      },

      // On success, replace optimistic task with real one
      onSuccess: (task) => {
        if (userId) {
          // Invalidate and refetch task lists
          queryClient.invalidateQueries({ queryKey: taskQueryKeys.lists() });
          queryClient.invalidateQueries({ queryKey: taskQueryKeys.stats(userId) });
        }
        options?.onCreateSuccess?.(task);
      },
    });

  /**
   * Update Task Mutation
   */
  const updateTaskMutation: UseMutationResult<
    Task,
    ApiErrorResponse,
    { taskId: number; input: UpdateTaskInput }
  > = useMutation<Task, ApiErrorResponse, { taskId: number; input: UpdateTaskInput }, { previousTasks?: Task[]; previousTask?: Task }>({
    mutationFn: ({ taskId, input }) => {
      if (!userId) {
        throw new Error('User ID is required');
      }
      return updateTask(userId, taskId, input);
    },

    // Optimistic update: Update task in cache immediately
    onMutate: async ({ taskId, input }) => {
      if (!userId) return {};

      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: taskQueryKeys.lists() });
      await queryClient.cancelQueries({ queryKey: taskQueryKeys.detail(userId, taskId) });

      // Snapshot previous values
      const previousTasks = queryClient.getQueryData<Task[]>(taskQueryKeys.list(userId));
      const previousTask = queryClient.getQueryData<Task>(
        taskQueryKeys.detail(userId, taskId)
      );

      // Optimistically update task list cache
      queryClient.setQueryData<Task[]>(taskQueryKeys.list(userId), (old = []) => {
        return old.map((task) => {
          if (task.id === taskId) {
            return {
              ...task,
              ...input,
              updated_at: new Date().toISOString(),
              _isUpdating: true,
            } as TaskWithUIState;
          }
          return task;
        });
      });

      // Optimistically update single task cache
      if (previousTask) {
        queryClient.setQueryData<Task>(taskQueryKeys.detail(userId, taskId), {
          ...previousTask,
          ...input,
          updated_at: new Date().toISOString(),
        });
      }

      // Return context for rollback
      return { previousTasks, previousTask };
    },

    // On error, rollback to previous state
    onError: (error, { taskId }, context) => {
      if (userId) {
        if (context?.previousTasks) {
          queryClient.setQueryData(taskQueryKeys.list(userId), context.previousTasks);
        }
        if (context?.previousTask) {
          queryClient.setQueryData(
            taskQueryKeys.detail(userId, taskId),
            context.previousTask
          );
        }
      }
      options?.onError?.(error);
    },

    // On success, replace optimistic update with real data
    onSuccess: (task, { taskId }) => {
      if (userId) {
        // Update caches with real data
        queryClient.setQueryData<Task[]>(taskQueryKeys.list(userId), (old = []) => {
          return old.map((t) => (t.id === taskId ? task : t));
        });
        queryClient.setQueryData(taskQueryKeys.detail(userId, taskId), task);

        // Invalidate stats
        queryClient.invalidateQueries({ queryKey: taskQueryKeys.stats(userId) });
      }
      options?.onUpdateSuccess?.(task);
    },
  });

  /**
   * Delete Task Mutation
   */
  const deleteTaskMutation: UseMutationResult<void, ApiErrorResponse, number> =
    useMutation<void, ApiErrorResponse, number, { previousTasks?: Task[] }>({
      mutationFn: (taskId: number) => {
        if (!userId) {
          throw new Error('User ID is required');
        }
        return deleteTask(userId, taskId);
      },

      // Optimistic update: Remove task from cache immediately
      onMutate: async (taskId) => {
        if (!userId) return {};

        // Cancel outgoing refetches
        await queryClient.cancelQueries({ queryKey: taskQueryKeys.lists() });

        // Snapshot previous value
        const previousTasks = queryClient.getQueryData<Task[]>(
          taskQueryKeys.list(userId)
        );

        // Optimistically remove task
        queryClient.setQueryData<Task[]>(taskQueryKeys.list(userId), (old = []) => {
          return old.map((task) =>
            task.id === taskId ? { ...task, _isDeleting: true } as TaskWithUIState : task
          );
        });

        // Return context for rollback
        return { previousTasks };
      },

      // On error, rollback to previous state
      onError: (error, _taskId, context) => {
        if (context?.previousTasks && userId) {
          queryClient.setQueryData(taskQueryKeys.list(userId), context.previousTasks);
        }
        options?.onError?.(error);
      },

      // On success, remove task completely
      onSuccess: (_data, taskId) => {
        if (userId) {
          // Remove task from cache
          queryClient.setQueryData<Task[]>(taskQueryKeys.list(userId), (old = []) => {
            return old.filter((task) => task.id !== taskId);
          });

          // Remove single task cache
          queryClient.removeQueries({ queryKey: taskQueryKeys.detail(userId, taskId) });

          // Invalidate stats
          queryClient.invalidateQueries({ queryKey: taskQueryKeys.stats(userId) });
        }
        options?.onDeleteSuccess?.(taskId);
      },
    });

  /**
   * Toggle Task Completion Mutation
   */
  const toggleCompletionMutation: UseMutationResult<
    Task,
    ApiErrorResponse,
    { taskId: number; completed: boolean }
  > = useMutation<Task, ApiErrorResponse, { taskId: number; completed: boolean }, { previousTasks?: Task[] }>({
    mutationFn: ({ taskId, completed }) => {
      if (!userId) {
        throw new Error('User ID is required');
      }
      return toggleTaskCompletion(userId, taskId, completed);
    },

    // Optimistic update: Toggle completion immediately
    onMutate: async ({ taskId, completed }) => {
      if (!userId) return {};

      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: taskQueryKeys.lists() });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData<Task[]>(taskQueryKeys.list(userId));

      // Optimistically toggle completion
      queryClient.setQueryData<Task[]>(taskQueryKeys.list(userId), (old = []) => {
        return old.map((task) =>
          task.id === taskId
            ? { ...task, completed, updated_at: new Date().toISOString() }
            : task
        );
      });

      // Return context for rollback
      return { previousTasks };
    },

    // On error, rollback to previous state
    onError: (error, _variables, context) => {
      if (context?.previousTasks && userId) {
        queryClient.setQueryData(taskQueryKeys.list(userId), context.previousTasks);
      }
      options?.onError?.(error);
    },

    // On success, update with real data
    onSuccess: (task, { taskId }) => {
      if (userId) {
        // Update task in cache
        queryClient.setQueryData<Task[]>(taskQueryKeys.list(userId), (old = []) => {
          return old.map((t) => (t.id === taskId ? task : t));
        });
        queryClient.setQueryData(taskQueryKeys.detail(userId, taskId), task);

        // Invalidate stats
        queryClient.invalidateQueries({ queryKey: taskQueryKeys.stats(userId) });
      }
      options?.onToggleSuccess?.(task);
    },
  });

  return {
    createTaskMutation,
    updateTaskMutation,
    deleteTaskMutation,
    toggleCompletionMutation,
  };
}

/**
 * Convenience hooks for individual mutations
 */

/**
 * Hook for creating tasks only
 */
export function useCreateTask(
  userId: number | null,
  options?: { onSuccess?: (task: Task) => void; onError?: (error: ApiErrorResponse) => void }
) {
  const { createTaskMutation } = useTaskMutations(userId, {
    onCreateSuccess: options?.onSuccess,
    onError: options?.onError,
  });
  return createTaskMutation;
}

/**
 * Hook for updating tasks only
 */
export function useUpdateTask(
  userId: number | null,
  options?: { onSuccess?: (task: Task) => void; onError?: (error: ApiErrorResponse) => void }
) {
  const { updateTaskMutation } = useTaskMutations(userId, {
    onUpdateSuccess: options?.onSuccess,
    onError: options?.onError,
  });
  return updateTaskMutation;
}

/**
 * Hook for deleting tasks only
 */
export function useDeleteTask(
  userId: number | null,
  options?: {
    onSuccess?: (taskId: number) => void;
    onError?: (error: ApiErrorResponse) => void;
  }
) {
  const { deleteTaskMutation } = useTaskMutations(userId, {
    onDeleteSuccess: options?.onSuccess,
    onError: options?.onError,
  });
  return deleteTaskMutation;
}

/**
 * Hook for toggling task completion only
 */
export function useToggleTaskCompletion(
  userId: number | null,
  options?: { onSuccess?: (task: Task) => void; onError?: (error: ApiErrorResponse) => void }
) {
  const { toggleCompletionMutation } = useTaskMutations(userId, {
    onToggleSuccess: options?.onSuccess,
    onError: options?.onError,
  });
  return toggleCompletionMutation;
}

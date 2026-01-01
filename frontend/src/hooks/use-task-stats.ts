/**
 * useTaskStats Hook - Phase 2 UI/UX
 *
 * Fetches task statistics for dashboard display
 * Uses React Query for caching and auto-refetch
 */

'use client';

import { useQuery } from '@tanstack/react-query';
import { useAuth } from './use-auth';

interface TaskStats {
  totalCount: number;
  completedCount: number;
  pendingCount: number;
  highPriorityCount: number;
  overdueCount: number;
}

export function useTaskStats() {
  const { user, isAuthenticated } = useAuth();

  const { data: stats, isLoading, error, refetch } = useQuery<TaskStats>({
    queryKey: ['taskStats', user?.id],
    queryFn: async () => {
      if (!isAuthenticated || !user) {
        throw new Error('User not authenticated');
      }

      // TODO: Replace with actual API call when backend endpoint is ready
      // For now, use the existing useTasks hook data
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${user.id}/tasks`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch tasks');
      }

      const tasks = await response.json();

      // Calculate statistics
      const totalCount = tasks.length;
      const completedCount = tasks.filter((t: any) => t.completed).length;
      const pendingCount = tasks.filter((t: any) => !t.completed).length;
      const highPriorityCount = tasks.filter((t: any) => t.priority === 'High').length;

      // Calculate overdue tasks
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const overdueCount = tasks.filter((t: any) => {
        if (t.completed || !t.due_date) return false;
        const dueDate = new Date(t.due_date);
        return dueDate < today;
      }).length;

      return {
        totalCount,
        completedCount,
        pendingCount,
        highPriorityCount,
        overdueCount,
      };
    },
    enabled: isAuthenticated && !!user,
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: true,
  });

  return {
    stats,
    isLoading,
    error,
    refetch,
  };
}

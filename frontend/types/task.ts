/**
 * Task Type Definitions
 *
 * TypeScript types for task entities and related data structures
 * aligned with the Phase 2 data model.
 */

/**
 * Priority Level Enum
 */
export type PriorityLevel = 'High' | 'Medium' | 'Low';

/**
 * Task Status (derived from completed field)
 */
export type TaskStatus = 'completed' | 'pending' | 'overdue';

/**
 * Task Entity (Database Model)
 *
 * Represents a task as stored in the database and returned by the API.
 * Includes all Phase 2 enhancements: priority, category, due_date.
 */
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  priority: PriorityLevel;
  category: string[];
  due_date: string | null; // ISO date format (YYYY-MM-DD)
  completed: boolean;
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime

  // Computed fields (returned by API but not stored in DB)
  is_overdue?: boolean;
  days_until_due?: number | null;
}

/**
 * Task Input for Creation
 *
 * Fields required/allowed when creating a new task.
 */
export interface CreateTaskInput {
  title: string; // Required, max 500 chars
  description?: string | null; // Optional, max 2000 chars
  priority?: PriorityLevel; // Optional, defaults to 'Medium'
  category?: string[]; // Optional, defaults to []
  due_date?: string | null; // Optional, ISO date format (YYYY-MM-DD)
}

/**
 * Task Input for Updates
 *
 * Fields allowed when updating an existing task.
 * All fields are optional.
 */
export interface UpdateTaskInput {
  title?: string;
  description?: string | null;
  priority?: PriorityLevel;
  category?: string[];
  due_date?: string | null;
  completed?: boolean;
}

/**
 * Task Filter Parameters
 *
 * Query parameters for filtering task lists.
 */
export interface TaskFilterParams {
  completed?: boolean; // Filter by completion status
  priority?: PriorityLevel; // Filter by priority level
  overdue?: boolean; // Show only overdue tasks
  category?: string; // Filter by category tag
  sortBy?: 'created_at' | 'due_date' | 'priority' | 'title';
  sortOrder?: 'asc' | 'desc';
}

/**
 * Task Statistics
 *
 * Aggregate statistics for dashboard display.
 */
export interface TaskStats {
  total: number;
  completed: number;
  pending: number;
  overdue: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
  completion_rate: number; // Percentage (0-100)
}

/**
 * Task with Local UI State
 *
 * Extended task type including local UI-only state
 * (e.g., optimistic updates, loading states).
 */
export interface TaskWithUIState extends Task {
  _isOptimistic?: boolean; // Optimistic update pending
  _isUpdating?: boolean; // Update in progress
  _isDeleting?: boolean; // Delete in progress
}

/**
 * Task Form State
 *
 * Form data structure for create/edit task forms.
 */
export interface TaskFormState {
  title: string;
  description: string;
  priority: PriorityLevel;
  category: string[];
  due_date: string | null; // ISO date format (YYYY-MM-DD)
}

/**
 * Task List Response
 *
 * API response for list endpoints.
 */
export interface TaskListResponse {
  tasks: Task[];
  total: number;
  page?: number;
  page_size?: number;
}

/**
 * Task Priority Color Map
 *
 * Maps priority levels to Tailwind CSS color classes.
 */
export const PRIORITY_COLORS: Record<PriorityLevel, string> = {
  High: 'bg-red-200 text-red-800 border-red-300',
  Medium: 'bg-orange-200 text-orange-800 border-orange-300',
  Low: 'bg-green-200 text-green-800 border-green-300',
};

/**
 * Task Priority Sort Order
 *
 * Numeric values for sorting tasks by priority (High → Low).
 */
export const PRIORITY_SORT_ORDER: Record<PriorityLevel, number> = {
  High: 3,
  Medium: 2,
  Low: 1,
};

/**
 * Default Task Form Values
 */
export const DEFAULT_TASK_FORM: TaskFormState = {
  title: '',
  description: '',
  priority: 'Medium',
  category: [],
  due_date: null,
};

/**
 * Type Guards
 */

/**
 * Check if a task is overdue
 */
export function isTaskOverdue(task: Task): boolean {
  if (!task.due_date || task.completed) {
    return false;
  }

  const dueDate = new Date(task.due_date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return dueDate < today;
}

/**
 * Get task status based on completed and due_date
 */
export function getTaskStatus(task: Task): TaskStatus {
  if (task.completed) {
    return 'completed';
  }

  if (isTaskOverdue(task)) {
    return 'overdue';
  }

  return 'pending';
}

/**
 * Calculate days until due date
 * Returns positive number for future dates, negative for past dates, null if no due date
 */
export function getDaysUntilDue(task: Task): number | null {
  if (!task.due_date) {
    return null;
  }

  const dueDate = new Date(task.due_date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  dueDate.setHours(0, 0, 0, 0);

  const diffTime = dueDate.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  return diffDays;
}

/**
 * Check if task matches filter criteria
 */
export function matchesFilter(task: Task, filter: TaskFilterParams): boolean {
  // Completed filter
  if (filter.completed !== undefined && task.completed !== filter.completed) {
    return false;
  }

  // Priority filter
  if (filter.priority !== undefined && task.priority !== filter.priority) {
    return false;
  }

  // Overdue filter
  if (filter.overdue !== undefined && filter.overdue !== isTaskOverdue(task)) {
    return false;
  }

  // Category filter
  if (filter.category !== undefined && !task.category.includes(filter.category)) {
    return false;
  }

  return true;
}

/**
 * Sort tasks by specified field and order
 */
export function sortTasks(
  tasks: Task[],
  sortBy: TaskFilterParams['sortBy'] = 'created_at',
  sortOrder: TaskFilterParams['sortOrder'] = 'desc'
): Task[] {
  const sorted = [...tasks].sort((a, b) => {
    let comparison = 0;

    switch (sortBy) {
      case 'created_at':
        comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        break;

      case 'due_date':
        // Tasks without due dates go to the end
        if (!a.due_date && !b.due_date) comparison = 0;
        else if (!a.due_date) comparison = 1;
        else if (!b.due_date) comparison = -1;
        else comparison = new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
        break;

      case 'priority':
        comparison = PRIORITY_SORT_ORDER[a.priority] - PRIORITY_SORT_ORDER[b.priority];
        break;

      case 'title':
        comparison = a.title.localeCompare(b.title);
        break;

      default:
        comparison = 0;
    }

    return sortOrder === 'asc' ? comparison : -comparison;
  });

  return sorted;
}

/**
 * Calculate task completion rate
 */
export function calculateCompletionRate(tasks: Task[]): number {
  if (tasks.length === 0) return 0;
  const completed = tasks.filter((t) => t.completed).length;
  return Math.round((completed / tasks.length) * 100);
}

/**
 * Get task statistics from a list of tasks
 */
export function getTaskStatistics(tasks: Task[]): TaskStats {
  const completed = tasks.filter((t) => t.completed).length;
  const pending = tasks.filter((t) => !t.completed).length;
  const overdue = tasks.filter((t) => isTaskOverdue(t)).length;
  const high_priority = tasks.filter((t) => t.priority === 'High').length;
  const medium_priority = tasks.filter((t) => t.priority === 'Medium').length;
  const low_priority = tasks.filter((t) => t.priority === 'Low').length;

  return {
    total: tasks.length,
    completed,
    pending,
    overdue,
    high_priority,
    medium_priority,
    low_priority,
    completion_rate: calculateCompletionRate(tasks),
  };
}

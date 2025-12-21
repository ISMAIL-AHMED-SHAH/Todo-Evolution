/**
 * Dashboard Page
 *
 * Main dashboard with task management functionality.
 * Features full CRUD operations for tasks:
 * - View all tasks
 * - Create new tasks
 * - Edit existing tasks
 * - Delete tasks
 * - Mark tasks complete/incomplete
 */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuth, useUserId } from '@/hooks/use-auth';
import { useTasks } from '@/hooks/use-tasks';
import { useTaskMutations } from '@/hooks/use-task-mutations';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import ProgressBar from '@/components/tasks/ProgressBar';
import TaskList from '@/components/tasks/TaskList';
import { TaskFormModal } from '@/components/tasks/TaskFormModal';
import { TaskForm } from '@/components/tasks/TaskForm';
import DashboardStats from '@/components/dashboard/DashboardStats';
import type { Task } from '@/types/task';
import type { CreateTaskFormData } from '@/lib/validations';

// Page transition animation variants
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

export default function DashboardPage() {
  const { user } = useAuth();
  const userId = useUserId();
  const { success, error: showError } = useToast();

  // Modal state for create and edit
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  // Fetch tasks
  const { data: tasks = [], isLoading, error } = useTasks(userId);

  // Get mutation handlers
  const {
    createTaskMutation,
    updateTaskMutation,
    deleteTaskMutation,
    toggleCompletionMutation
  } = useTaskMutations(userId, {
    onCreateSuccess: (task) => {
      setIsCreateModalOpen(false);
      success(`Task "${task.title}" created successfully!`, 'Task Created');
    },
    onUpdateSuccess: (task) => {
      setIsEditModalOpen(false);
      setSelectedTask(null);
      success(`Task "${task.title}" updated successfully!`, 'Task Updated');
    },
    onDeleteSuccess: () => {
      success('Task deleted successfully!', 'Task Deleted');
    },
    onError: (err) => {
      showError(err?.error?.message || 'An error occurred. Please try again.', 'Error');
    }
  });

  // Calculate progress statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((task) => task.completed).length;

  // Handle create task
  const handleCreateTask = (data: CreateTaskFormData) => {
    createTaskMutation.mutate(data);
  };

  // Handle edit task
  const handleEditTask = (data: CreateTaskFormData) => {
    if (selectedTask) {
      updateTaskMutation.mutate({
        taskId: selectedTask.id,
        input: data
      });
    }
  };

  // Handle toggle completion
  const handleToggleComplete = (taskId: number) => {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      toggleCompletionMutation.mutate({ taskId, completed: !task.completed });
    }
  };

  // Handle delete
  const handleDelete = (taskId: number) => {
    deleteTaskMutation.mutate(taskId);
  };

  // Handle edit button click
  const handleEdit = (task: Task) => {
    setSelectedTask(task);
    setIsEditModalOpen(true);
  };

  return (
    <ProtectedRoute>
      <motion.div
        variants={pageVariants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={{ duration: 0.3 }}
        className="container mx-auto px-3 sm:px-4 py-4 sm:py-8 max-w-7xl"
      >
        {/* Header Section */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">
              Dashboard
            </h1>
            <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 mt-1">
              Welcome back, {user?.email}!
            </p>
          </div>

          {/* Add Task Button */}
          <Button
            onClick={() => setIsCreateModalOpen(true)}
            className="w-full sm:w-auto bg-teal-600 hover:bg-teal-700 text-white min-h-[44px]"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Task
          </Button>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="space-y-4 sm:space-y-6">
            <Skeleton className="h-20 sm:h-24 w-full" />
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-40 sm:h-48 w-full" />
              ))}
            </div>
          </div>
        )}

        {/* Error State */}
        {error && !isLoading && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>
              {error?.error?.message || 'Failed to load tasks. Please try again later.'}
            </AlertDescription>
          </Alert>
        )}

        {/* Success State */}
        {!isLoading && !error && (
          <>
            {/* Dashboard Statistics */}
            <DashboardStats tasks={tasks} className="mb-6 sm:mb-8" />

            {/* Progress Bar */}
            <ProgressBar
              totalTasks={totalTasks}
              completedTasks={completedTasks}
              className="mb-4 sm:mb-8"
            />

            {/* Task List */}
            <TaskList
              tasks={tasks}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
              onEdit={handleEdit}
            />
          </>
        )}

        {/* Create Task Modal */}
        <TaskFormModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          mode="create"
        >
          <TaskForm
            mode="create"
            onSubmit={handleCreateTask}
            onCancel={() => setIsCreateModalOpen(false)}
            isLoading={createTaskMutation.isPending}
          />
        </TaskFormModal>

        {/* Edit Task Modal */}
        <TaskFormModal
          isOpen={isEditModalOpen}
          onClose={() => {
            setIsEditModalOpen(false);
            setSelectedTask(null);
          }}
          mode="edit"
          task={selectedTask}
        >
          <TaskForm
            mode="edit"
            task={selectedTask}
            onSubmit={handleEditTask}
            onCancel={() => {
              setIsEditModalOpen(false);
              setSelectedTask(null);
            }}
            isLoading={updateTaskMutation.isPending}
          />
        </TaskFormModal>
      </motion.div>
    </ProtectedRoute>
  );
}

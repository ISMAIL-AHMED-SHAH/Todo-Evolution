"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useTasks } from "@/hooks/use-tasks";
import { useUserId } from "@/hooks/use-auth";
import { useTaskMutations } from "@/hooks/use-task-mutations";
import ProgressBar from "@/components/tasks/ProgressBar";
import TaskList from "@/components/tasks/TaskList";
import { TaskFormModal } from "@/components/tasks/TaskFormModal";
import { TaskForm } from "@/components/tasks/TaskForm";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import type { Task } from "@/types/task";
import type { CreateTaskFormData } from "@/lib/validations";

// Page transition animation variants
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

/**
 * Tasks List Page
 *
 * Main page for displaying all user tasks with progress tracking.
 * Features:
 * - Progress bar showing task completion statistics
 * - Task list with all task metadata
 * - Loading and error states
 * - Framer Motion page transitions
 * - Optimistic updates for task completion and deletion
 * - T118: Task editing with modal (Phase 7)
 */
export default function TasksPage() {
  const userId = useUserId();

  // T118: State for edit modal
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  // Fetch tasks using React Query
  const { data: tasks = [], isLoading, error } = useTasks(userId);

  // Get mutation handlers for optimistic updates
  const { toggleCompletionMutation, deleteTaskMutation, updateTaskMutation } = useTaskMutations(userId, {
    onUpdateSuccess: () => {
      setIsEditModalOpen(false);
      setSelectedTask(null);
    }
  });

  // Calculate progress statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((task) => task.completed).length;

  // Handle completion toggle with optimistic update
  const handleToggleComplete = (taskId: number) => {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
      toggleCompletionMutation.mutate({ taskId, completed: !task.completed });
    }
  };

  // Handle delete with optimistic update
  const handleDelete = (taskId: number) => {
    deleteTaskMutation.mutate(taskId);
  };

  // T118: Handle edit button click - open modal with selected task
  const handleEdit = (task: Task) => {
    setSelectedTask(task);
    setIsEditModalOpen(true);
  };

  // T118: Handle edit form submission
  const handleEditSubmit = (data: CreateTaskFormData) => {
    if (selectedTask) {
      updateTaskMutation.mutate({
        taskId: selectedTask.id,
        input: data
      });
    }
  };

  // T118: Handle edit modal close
  const handleEditCancel = () => {
    setIsEditModalOpen(false);
    setSelectedTask(null);
  };

  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.3 }}
      className="container mx-auto px-3 sm:px-4 py-4 sm:py-8 max-w-7xl"
    >
      {/* Page Title */}
      <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-4 sm:mb-6 md:mb-8">My Tasks</h1>

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
            {error?.error?.message || "Failed to load tasks. Please try again later."}
          </AlertDescription>
        </Alert>
      )}

      {/* Success State */}
      {!isLoading && !error && (
        <>
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

      {/* T118: Edit Task Modal (Phase 7) */}
      <TaskFormModal
        isOpen={isEditModalOpen}
        onClose={handleEditCancel}
        mode="edit"
        task={selectedTask}
      >
        <TaskForm
          mode="edit"
          task={selectedTask}
          onSubmit={handleEditSubmit}
          onCancel={handleEditCancel}
          isLoading={updateTaskMutation.isPending}
        />
      </TaskFormModal>
    </motion.div>
  );
}

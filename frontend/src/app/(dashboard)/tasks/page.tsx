"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { useTasks } from "@/hooks/use-tasks";
import { useUserId } from "@/hooks/use-auth";
import { useTaskMutations } from "@/hooks/use-task-mutations";
import { useToast } from "@/hooks/use-toast";
import ProgressBar from "@/components/tasks/ProgressBar";
import { TaskFormModal } from "@/components/tasks/TaskFormModal";
import { TaskForm } from "@/components/tasks/TaskForm";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  AlertCircle,
  CheckCircle2,
  Circle,
  Calendar,
  Tag,
  Edit,
  Trash2,
  Clock
} from "lucide-react";
import { format, isPast } from "date-fns";
import type { Task } from "@/types/task";
import type { CreateTaskFormData } from "@/lib/validations";
import { cn } from "@/lib/utils";

// Page transition animation variants
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

// Priority color mapping
const priorityColors = {
  High: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300 border-red-300 dark:border-red-800",
  Medium: "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300 border-orange-300 dark:border-orange-800",
  Low: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300 border-green-300 dark:border-green-800",
};

// Task card animation variants
const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.05,
      type: 'spring',
      stiffness: 300,
      damping: 25,
    },
  }),
};

/**
 * Tasks List Page
 *
 * Beautiful task management page with tabs for filtering tasks by status.
 * Features:
 * - Tabbed interface (All, Pending, Completed)
 * - Progress bar showing task completion statistics
 * - Card-based task display with rich metadata
 * - Status badges, priority indicators, due dates
 * - Optimistic updates for all task operations
 */
export default function TasksPage() {
  const userId = useUserId();
  const { success, error: showError } = useToast();
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  // Fetch tasks using React Query
  const { data: tasks = [], isLoading, error } = useTasks(userId);

  // Get mutation handlers with toast notifications
  const {
    toggleCompletionMutation,
    deleteTaskMutation,
    updateTaskMutation
  } = useTaskMutations(userId, {
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

  // Filter tasks by status
  const pendingTasks = useMemo(() => tasks.filter(t => !t.completed), [tasks]);
  const completedTasks = useMemo(() => tasks.filter(t => t.completed), [tasks]);

  // Calculate progress statistics
  const totalTasks = tasks.length;
  const completedCount = completedTasks.length;

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

  // Handle edit button click - open modal with selected task
  const handleEdit = (task: Task) => {
    setSelectedTask(task);
    setIsEditModalOpen(true);
  };

  // Handle edit form submission
  const handleEditSubmit = (data: CreateTaskFormData) => {
    if (selectedTask) {
      updateTaskMutation.mutate({
        taskId: selectedTask.id,
        input: data
      });
    }
  };

  // Handle edit modal close
  const handleEditCancel = () => {
    setIsEditModalOpen(false);
    setSelectedTask(null);
  };

  // Render a single task card
  const renderTaskCard = (task: Task, index: number) => {
    const isOverdue = task.due_date && !task.completed && isPast(new Date(task.due_date));

    return (
      <motion.div
        key={task.id}
        custom={index}
        variants={cardVariants}
        initial="hidden"
        animate="visible"
        className={cn(
          "group relative bg-white dark:bg-gray-800 rounded-lg border-2 p-4 sm:p-5 transition-all duration-200",
          task.completed
            ? "border-gray-200 dark:border-gray-700 opacity-75"
            : "border-gray-300 dark:border-gray-600 hover:border-teal-500 dark:hover:border-teal-500 hover:shadow-lg"
        )}
      >
        {/* Status Icon & Title */}
        <div className="flex items-start gap-3 mb-3">
          <button
            onClick={() => handleToggleComplete(task.id)}
            className="mt-0.5 flex-shrink-0 transition-transform hover:scale-110"
            aria-label={task.completed ? "Mark as pending" : "Mark as complete"}
          >
            {task.completed ? (
              <CheckCircle2 className="h-6 w-6 text-teal-600 dark:text-teal-400" />
            ) : (
              <Circle className="h-6 w-6 text-gray-400 dark:text-gray-500 hover:text-teal-600 dark:hover:text-teal-400" />
            )}
          </button>

          <div className="flex-1 min-w-0">
            <h3
              className={cn(
                "text-base sm:text-lg font-semibold mb-1",
                task.completed
                  ? "line-through text-gray-500 dark:text-gray-400"
                  : "text-gray-900 dark:text-white"
              )}
            >
              {task.title}
            </h3>

            {task.description && (
              <p className="text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
                {task.description}
              </p>
            )}
          </div>
        </div>

        {/* Metadata Row */}
        <div className="flex flex-wrap items-center gap-2 mb-3">
          {/* Priority Badge */}
          <Badge variant="outline" className={cn("text-xs font-medium border", priorityColors[task.priority as keyof typeof priorityColors])}>
            {task.priority}
          </Badge>

          {/* Due Date */}
          {task.due_date && (
            <Badge
              variant="outline"
              className={cn(
                "text-xs font-medium border",
                isOverdue
                  ? "bg-red-50 text-red-700 border-red-300 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800"
                  : "bg-blue-50 text-blue-700 border-blue-300 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800"
              )}
            >
              <Calendar className="h-3 w-3 mr-1" />
              {format(new Date(task.due_date), 'MMM d, yyyy')}
            </Badge>
          )}

          {/* Status Badge */}
          <Badge
            variant="outline"
            className={cn(
              "text-xs font-medium border",
              task.completed
                ? "bg-green-50 text-green-700 border-green-300 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800"
                : "bg-gray-50 text-gray-700 border-gray-300 dark:bg-gray-900/20 dark:text-gray-300 dark:border-gray-700"
            )}
          >
            {task.completed ? "Completed" : "Pending"}
          </Badge>
        </div>

        {/* Categories */}
        {task.category && task.category.length > 0 && (
          <div className="flex flex-wrap items-center gap-1.5 mb-3">
            <Tag className="h-3.5 w-3.5 text-gray-400 dark:text-gray-500" />
            {task.category.slice(0, 3).map((cat, i) => (
              <Badge
                key={i}
                variant="secondary"
                className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-600"
              >
                {cat}
              </Badge>
            ))}
            {task.category.length > 3 && (
              <span className="text-xs text-gray-500 dark:text-gray-400">
                +{task.category.length - 3} more
              </span>
            )}
          </div>
        )}

        <Separator className="my-3" />

        {/* Action Buttons */}
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
            <Clock className="h-3.5 w-3.5" />
            <span>
              {format(new Date(task.created_at), 'MMM d')}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleEdit(task)}
              className="h-8 px-3 text-gray-700 dark:text-gray-300 hover:text-teal-600 dark:hover:text-teal-400 hover:bg-teal-50 dark:hover:bg-teal-900/20"
            >
              <Edit className="h-3.5 w-3.5 mr-1" />
              Edit
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleDelete(task.id)}
              className="h-8 px-3 text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
            >
              <Trash2 className="h-3.5 w-3.5 mr-1" />
              Delete
            </Button>
          </div>
        </div>
      </motion.div>
    );
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
      <div className="mb-6 sm:mb-8">
        <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
          My Tasks
        </h1>
        <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300">
          Manage and track all your tasks in one place
        </p>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="space-y-4 sm:space-y-6">
          <Skeleton className="h-20 sm:h-24 w-full" />
          <Skeleton className="h-12 w-full" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <Skeleton key={i} className="h-48 w-full" />
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
            completedTasks={completedCount}
            className="mb-6 sm:mb-8"
          />

          {/* Tabbed Task View */}
          <Tabs defaultValue="all" className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-6 bg-gray-100 dark:bg-gray-800">
              <TabsTrigger value="all" className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700">
                All ({totalTasks})
              </TabsTrigger>
              <TabsTrigger value="pending" className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700">
                Pending ({pendingTasks.length})
              </TabsTrigger>
              <TabsTrigger value="completed" className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700">
                Completed ({completedTasks.length})
              </TabsTrigger>
            </TabsList>

            {/* All Tasks Tab */}
            <TabsContent value="all" className="mt-0">
              {tasks.length === 0 ? (
                <div className="text-center py-12">
                  <Circle className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    No tasks yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Create your first task to get started!
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {tasks.map((task, index) => renderTaskCard(task, index))}
                </div>
              )}
            </TabsContent>

            {/* Pending Tasks Tab */}
            <TabsContent value="pending" className="mt-0">
              {pendingTasks.length === 0 ? (
                <div className="text-center py-12">
                  <CheckCircle2 className="h-16 w-16 text-teal-500 dark:text-teal-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    All caught up!
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    No pending tasks at the moment
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {pendingTasks.map((task, index) => renderTaskCard(task, index))}
                </div>
              )}
            </TabsContent>

            {/* Completed Tasks Tab */}
            <TabsContent value="completed" className="mt-0">
              {completedTasks.length === 0 ? (
                <div className="text-center py-12">
                  <Clock className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    No completed tasks
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Complete some tasks to see them here
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {completedTasks.map((task, index) => renderTaskCard(task, index))}
                </div>
              )}
            </TabsContent>
          </Tabs>
        </>
      )}

      {/* Edit Task Modal */}
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

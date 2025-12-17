"use client";

import { motion } from "framer-motion";
import { Calendar, Clock, Trash2, Edit } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import PriorityBadge from "./PriorityBadge";
import CategoryBadge from "./CategoryBadge";
import StatusBadge from "./StatusBadge";
import { cn } from "@/lib/utils";
import type { Task } from "@/types/task";
import { useState } from "react";

interface TaskCardProps {
  task: Task;
  onToggleComplete?: (taskId: number) => void;
  onDelete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  className?: string;
}

/**
 * Format a date string to a readable format
 */
function formatDate(dateString: string | null): string {
  if (!dateString) return "No date set";

  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

/**
 * Format a timestamp to a relative time string
 */
function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (diffInSeconds < 60) return "just now";
  if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes} ${minutes === 1 ? "minute" : "minutes"} ago`;
  }
  if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours} ${hours === 1 ? "hour" : "hours"} ago`;
  }

  const days = Math.floor(diffInSeconds / 86400);
  if (days < 30) return `${days} ${days === 1 ? "day" : "days"} ago`;

  return formatDate(dateString);
}

/**
 * TaskCard Component
 *
 * Displays a task with all metadata, completion toggle, edit button, and delete button.
 * Features:
 * - T096: Completion toggle with optimistic updates
 * - T097: Strikethrough styling for completed tasks
 * - T098: Delete button with confirmation dialog
 * - T101: Hover effects with Framer Motion
 * - T118: Edit button to open edit modal (Phase 7)
 */
export default function TaskCard({ task, onToggleComplete, onDelete, onEdit, className }: TaskCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const isCompleted = task.completed;

  // T096: Handle completion toggle with optimistic updates
  const handleToggleComplete = () => {
    if (onToggleComplete) {
      onToggleComplete(task.id);
    }
  };

  // T118: Handle edit button click (Phase 7)
  const handleEdit = () => {
    if (onEdit) {
      onEdit(task);
    }
  };

  // T098: Handle delete with confirmation
  const handleDelete = () => {
    setIsDeleting(true);
    if (onDelete) {
      onDelete(task.id);
    }
  };

  return (
    <motion.div
      // T101 + T145: Hover effects with Framer Motion (performance optimized)
      whileHover={{ scale: 1.02, willChange: 'transform' }}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
      className={cn("w-full", className)}
      style={{ willChange: 'auto' }}
    >
      <Card className={cn("overflow-hidden", isCompleted && "opacity-75")}>
        <CardHeader className="pb-3 px-3 sm:px-4 md:px-6 pt-3 sm:pt-4 md:pt-6">
          <div className="flex items-start justify-between gap-2 sm:gap-2.5 md:gap-3">
            <div className="flex items-start gap-2 sm:gap-3 flex-1 min-w-0">
              {/* T096: Completion toggle checkbox - min 44px touch target */}
              <Checkbox
                checked={isCompleted}
                onCheckedChange={handleToggleComplete}
                className="mt-1 min-w-[20px] min-h-[20px]"
                aria-label={`Mark task "${task.title}" as ${isCompleted ? 'incomplete' : 'complete'}`}
              />
              <div className="flex-1 min-w-0">
                {/* T097: Strikethrough styling for completed tasks */}
                <CardTitle
                  className={cn(
                    "text-base sm:text-[1.0625rem] md:text-lg font-semibold break-words",
                    isCompleted && "line-through text-muted-foreground"
                  )}
                >
                  {task.title}
                </CardTitle>
              </div>
            </div>
            <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
              <StatusBadge completed={isCompleted} />
              {/* T118: Edit button (Phase 7) - 44px min touch target */}
              <Button
                variant="ghost"
                size="icon"
                onClick={handleEdit}
                className="h-9 w-9 sm:h-8 sm:w-8 text-muted-foreground hover:text-blue-600"
                title="Edit task"
                aria-label={`Edit task: ${task.title}`}
              >
                <Edit className="h-4 w-4" aria-hidden="true" />
              </Button>
              {/* T098: Delete button with confirmation dialog - 44px min touch target */}
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-9 w-9 sm:h-8 sm:w-8 text-muted-foreground hover:text-destructive"
                    title="Delete task"
                    aria-label={`Delete task: ${task.title}`}
                  >
                    <Trash2 className="h-4 w-4" aria-hidden="true" />
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent className="w-[95vw] max-w-md">
                  <AlertDialogHeader>
                    <AlertDialogTitle>Delete Task</AlertDialogTitle>
                    <AlertDialogDescription className="break-words">
                      Are you sure you want to delete "{task.title}"? This action cannot be undone.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter className="flex-col sm:flex-row gap-2">
                    <AlertDialogCancel className="w-full sm:w-auto min-h-[44px]">Cancel</AlertDialogCancel>
                    <AlertDialogAction onClick={handleDelete} className="w-full sm:w-auto min-h-[44px] bg-destructive text-destructive-foreground hover:bg-destructive/90">
                      Delete
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </div>

          {task.description && (
            <CardDescription
              className={cn(
                "mt-2 text-sm ml-6 sm:ml-8 break-words",
                // T097: Strikethrough for description too
                isCompleted && "line-through"
              )}
            >
              {task.description}
            </CardDescription>
          )}
        </CardHeader>

        <CardContent className="space-y-3 sm:space-y-3.5 md:space-y-4 px-3 sm:px-4 md:px-6 pb-3 sm:pb-4 md:pb-6">
          {/* Priority and Categories */}
          <div className="flex flex-wrap gap-2 ml-6 sm:ml-8">
            <PriorityBadge priority={task.priority} />
            {task.category && task.category.length > 0 && (
              <CategoryBadge categories={task.category} />
            )}
          </div>

          {/* Due Date */}
          {task.due_date && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground ml-6 sm:ml-8">
              <Calendar className="h-4 w-4 flex-shrink-0" />
              <span className="break-words">Due: {formatDate(task.due_date)}</span>
            </div>
          )}

          {/* Timestamps */}
          <div className="flex flex-col gap-1 text-xs text-muted-foreground ml-6 sm:ml-8">
            <div className="flex items-center gap-2">
              <Clock className="h-3 w-3 flex-shrink-0" />
              <span>Created {formatRelativeTime(task.created_at)}</span>
            </div>
            {task.updated_at !== task.created_at && (
              <div className="flex items-center gap-2">
                <Clock className="h-3 w-3 flex-shrink-0" />
                <span>Updated {formatRelativeTime(task.updated_at)}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

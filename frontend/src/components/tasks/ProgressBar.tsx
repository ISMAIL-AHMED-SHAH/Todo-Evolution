"use client";

import React from "react";
import { motion } from "framer-motion";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface ProgressBarProps {
  totalTasks: number;
  completedTasks: number;
  className?: string;
}

/**
 * ProgressBar Component
 *
 * Displays an animated progress bar showing task completion status.
 * Handles edge cases like zero tasks and 100% completion with special styling.
 *
 * @param totalTasks - Total number of tasks
 * @param completedTasks - Number of completed tasks
 * @param className - Optional additional CSS classes
 */
export default function ProgressBar({
  totalTasks,
  completedTasks,
  className,
}: ProgressBarProps) {
  // Edge case: no tasks yet
  if (totalTasks === 0) {
    return (
      <motion.div
        className={cn(
          "text-center py-4 text-muted-foreground text-sm",
          className
        )}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        No tasks yet
      </motion.div>
    );
  }

  // Calculate percentage (T095: Progress calculation implementation)
  const percentage = Math.round((completedTasks / totalTasks) * 100);
  const isComplete = percentage === 100;

  return (
    <div className={cn("space-y-2 px-2 sm:px-0", className)}>
      {/* Progress Bar */}
      <div className="relative">
        <Progress
          value={percentage}
          className={cn(
            "h-2 sm:h-3 transition-colors duration-300",
            isComplete && "bg-green-100 dark:bg-green-950"
          )}
        />
      </div>

      {/* Percentage Text */}
      <motion.div
        className="flex items-center justify-between text-xs sm:text-sm gap-2"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.2 }}
      >
        <span
          className={cn(
            "font-medium transition-colors duration-300 truncate",
            isComplete
              ? "text-green-600 dark:text-green-400"
              : "text-foreground"
          )}
        >
          {isComplete ? "All Complete!" : `${percentage}% Complete`}
        </span>
        <span className="text-muted-foreground text-xs flex-shrink-0">
          {completedTasks} / {totalTasks} tasks
        </span>
      </motion.div>

      {/* Success celebration indicator */}
      {isComplete && (
        <motion.div
          className="flex items-center justify-center gap-2 text-green-600 dark:text-green-400 text-xs sm:text-sm font-medium"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4, delay: 0.4 }}
        >
          <span className="text-base sm:text-lg">🎉</span>
          <span>Great work!</span>
        </motion.div>
      )}
    </div>
  );
}

"use client";

import { motion } from "framer-motion";
import type { Task } from "@/types/task";
import TaskCard from "./TaskCard";

interface TaskListProps {
  tasks: Task[];
  onToggleComplete?: (taskId: number) => void;
  onDelete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
}

// T100 + T145: Framer Motion animation variants (performance optimized)
const listVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05, // Reduced from 0.1 for faster animation
      delayChildren: 0.05,   // Reduced from 0.1
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20, willChange: 'opacity, transform' },
  visible: {
    opacity: 1,
    y: 0,
    willChange: 'auto',
    transition: {
      duration: 0.25,  // Reduced from 0.3
      ease: [0.4, 0, 0.2, 1] as const, // Custom cubic-bezier for smoother motion
    },
  },
};

/**
 * TaskList Component
 *
 * Displays a list of tasks with animations and responsive layout.
 * Features:
 * - T099: Empty state message "No tasks yet..."
 * - T100: Framer Motion stagger animation for list items
 * - T102: Responsive layout (stack on mobile, grid on desktop)
 * - T118: Support for editing tasks (Phase 7)
 */
export default function TaskList({ tasks, onToggleComplete, onDelete, onEdit }: TaskListProps) {
  // T099: Empty state implementation
  if (tasks.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex flex-col items-center justify-center py-12 sm:py-16 px-4 text-center"
      >
        <div className="text-gray-400 text-5xl sm:text-6xl mb-3 sm:mb-4">📋</div>
        <h3 className="text-lg sm:text-xl font-semibold text-gray-700 mb-2">No tasks yet...</h3>
        <p className="text-sm sm:text-base text-gray-500 max-w-md">
          Get started by creating your first task. Stay organized and productive!
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      // T100: Apply stagger animation to container
      variants={listVariants}
      initial="hidden"
      animate="visible"
      // T102 + T137: Responsive grid layout
      // Mobile: 1 column (grid-cols-1)
      // Tablet: 2 columns (md:grid-cols-2)
      // Desktop: 3 columns (lg:grid-cols-3)
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 md:gap-5 w-full"
    >
      {tasks.map((task) => (
        <motion.div
          key={task.id}
          // T100: Apply stagger animation to each item
          variants={itemVariants}
          layout
        >
          <TaskCard
            task={task}
            onToggleComplete={onToggleComplete}
            onDelete={onDelete}
            onEdit={onEdit}
          />
        </motion.div>
      ))}
    </motion.div>
  );
}

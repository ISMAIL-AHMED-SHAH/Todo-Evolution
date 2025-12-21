/**
 * DashboardStats Component
 *
 * Displays task statistics and insights in an attractive card layout.
 * Features:
 * - Total tasks count
 * - Completed tasks count
 * - Pending tasks count
 * - Completion rate percentage
 * - High priority tasks count
 * - Responsive grid layout
 * - Dark mode support
 * - Icon-based visual design
 */

'use client';

import { CheckCircle2, Circle, ListTodo, TrendingUp, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import type { Task } from '@/types/task';
import { cn } from '@/lib/utils';

interface DashboardStatsProps {
  tasks: Task[];
  className?: string;
}

interface StatCardProps {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  color: string;
  index: number;
}

/**
 * Animation variants for stat cards
 */
const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.1,
      type: 'spring',
      stiffness: 300,
      damping: 25,
    },
  }),
};

/**
 * Individual stat card component
 */
function StatCard({ title, value, icon, color, index }: StatCardProps) {
  return (
    <motion.div
      custom={index}
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      className={cn(
        'bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 sm:p-6',
        'shadow-sm hover:shadow-md transition-shadow duration-200'
      )}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
            {title}
          </p>
          <p className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
            {value}
          </p>
        </div>
        <div className={cn('p-3 rounded-full', color)}>
          {icon}
        </div>
      </div>
    </motion.div>
  );
}

export default function DashboardStats({ tasks, className }: DashboardStatsProps) {
  // Calculate statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0
    ? Math.round((completedTasks / totalTasks) * 100)
    : 0;
  const highPriorityTasks = tasks.filter(
    task => task.priority === 'High' && !task.completed
  ).length;

  return (
    <div className={cn('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4', className)}>
      <StatCard
        title="Total Tasks"
        value={totalTasks}
        icon={<ListTodo className="h-6 w-6 text-blue-600 dark:text-blue-400" />}
        color="bg-blue-100 dark:bg-blue-900/30"
        index={0}
      />

      <StatCard
        title="Completed"
        value={completedTasks}
        icon={<CheckCircle2 className="h-6 w-6 text-green-600 dark:text-green-400" />}
        color="bg-green-100 dark:bg-green-900/30"
        index={1}
      />

      <StatCard
        title="Pending"
        value={pendingTasks}
        icon={<Circle className="h-6 w-6 text-orange-600 dark:text-orange-400" />}
        color="bg-orange-100 dark:bg-orange-900/30"
        index={2}
      />

      <StatCard
        title="Completion"
        value={`${completionRate}%`}
        icon={<TrendingUp className="h-6 w-6 text-purple-600 dark:text-purple-400" />}
        color="bg-purple-100 dark:bg-purple-900/30"
        index={3}
      />

      <StatCard
        title="High Priority"
        value={highPriorityTasks}
        icon={<AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400" />}
        color="bg-red-100 dark:bg-red-900/30"
        index={4}
      />
    </div>
  );
}

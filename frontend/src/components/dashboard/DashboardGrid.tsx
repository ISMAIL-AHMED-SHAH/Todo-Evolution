/**
 * DashboardGrid Component - Phase 2 UI/UX
 *
 * Grid of 5 interactive action cards:
 * 1. Add Task (Mint Green) - Opens modal
 * 2. View Tasks (Purple) - Navigate to task list
 * 3. Update Task (Sky Blue) - Navigate to task list
 * 4. Complete/Pending (Pink) - Shows counts
 * 5. Delete Task (Coral) - Navigate to task list
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import DashboardCard from './DashboardCard';
import { TaskFormModal } from '@/components/tasks/TaskFormModal';
import { TaskForm } from '@/components/tasks/TaskForm';
import { useTaskStats } from '../../hooks/use-task-stats';
import { useCreateTask } from '@/hooks/use-task-mutations';
import { useAuth } from '@/hooks/use-auth';
import { useToast } from '../../hooks/use-toast';
import type { CreateTaskFormData } from '@/lib/validations';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
    },
  },
};

export default function DashboardGrid() {
  const router = useRouter();
  const { user } = useAuth();
  const { stats, isLoading } = useTaskStats();
  const { toast } = useToast();
  const [isAddTaskModalOpen, setIsAddTaskModalOpen] = useState(false);

  // Create task mutation with toast notifications
  const createTaskMutation = useCreateTask(user?.id || null, {
    onSuccess: (task) => {
      toast({
        title: 'Task Created',
        description: `Task "${task.title}" created successfully!`,
      });
      setIsAddTaskModalOpen(false);
    },
    onError: (err) => {
      toast({
        title: 'Error',
        description: err?.error?.message || 'Failed to create task. Please try again.',
        variant: 'destructive',
      });
    },
  });

  const cards = [
    {
      title: 'Add Task',
      emoji: '➕',
      backgroundColor: 'bg-emerald-200',
      onClick: () => setIsAddTaskModalOpen(true),
    },
    {
      title: 'View Tasks',
      emoji: '📋',
      backgroundColor: 'bg-purple-200',
      onClick: () => router.push('/tasks'),
    },
    {
      title: 'Update Task',
      emoji: '✏️',
      backgroundColor: 'bg-sky-200',
      onClick: () => router.push('/tasks'),
    },
    {
      title: 'Complete / Pending',
      emoji: '✅',
      backgroundColor: 'bg-pink-200',
      badge: isLoading ? 'Loading...' : `${stats?.completedCount || 0} done, ${stats?.pendingCount || 0} pending`,
      onClick: () => router.push('/tasks'),
    },
    {
      title: 'Delete Task',
      emoji: '🗑️',
      backgroundColor: 'bg-orange-200',
      onClick: () => router.push('/tasks'),
    },
  ];

  /**
   * Handle task creation submission
   * T113: Form submission with toast success message
   */
  const handleCreateTask = (data: CreateTaskFormData) => {
    createTaskMutation.mutate(data);
  };

  /**
   * Handle modal close
   * T114: Modal close on cancel
   */
  const handleCloseModal = () => {
    setIsAddTaskModalOpen(false);
  };

  return (
    <>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 sm:gap-5 md:gap-6"
      >
        {cards.map((card, index) => (
          <motion.div key={index} variants={itemVariants}>
            <DashboardCard {...card} />
          </motion.div>
        ))}
      </motion.div>

      {/* Task Creation Modal with T111, T112, T113, T114, T115, T116 */}
      <TaskFormModal
        isOpen={isAddTaskModalOpen}
        onClose={handleCloseModal}
        mode="create"
      >
        <TaskForm
          mode="create"
          onSubmit={handleCreateTask}
          onCancel={handleCloseModal}
          isLoading={createTaskMutation.isPending}
        />
      </TaskFormModal>
    </>
  );
}

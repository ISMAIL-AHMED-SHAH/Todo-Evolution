/**
 * TaskFormModal Component
 *
 * Modal wrapper for task creation and editing forms.
 * Provides slide-in animation with Framer Motion and manages form state.
 */

'use client';

import { motion, AnimatePresence } from 'framer-motion';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import type { Task } from '@/types/task';

interface TaskFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  mode: 'create' | 'edit';
  task?: Task | null;
  children: React.ReactNode;
}

/**
 * Modal animation variants
 */
const modalVariants = {
  hidden: {
    opacity: 0,
    scale: 0.95,
    y: 20,
  },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      type: 'spring' as const,
      stiffness: 300,
      damping: 30,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    y: 20,
    transition: {
      duration: 0.2,
    },
  },
};

export function TaskFormModal({
  isOpen,
  onClose,
  mode,
  task,
  children,
}: TaskFormModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="w-[95vw] max-w-[600px] max-h-[90vh] overflow-y-auto">
        <AnimatePresence mode="wait">
          {isOpen && (
            <motion.div
              variants={modalVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
            >
              <DialogHeader>
                <DialogTitle className="text-xl sm:text-2xl font-bold">
                  {mode === 'create' ? 'Create New Task' : 'Edit Task'}
                </DialogTitle>
                <DialogDescription className="text-sm">
                  {mode === 'create'
                    ? 'Fill out the form below to create a new task. All fields except title are optional.'
                    : 'Update the task details below and click Save Changes.'}
                </DialogDescription>
              </DialogHeader>

              <div className="mt-4 sm:mt-6">
                {children}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </DialogContent>
    </Dialog>
  );
}

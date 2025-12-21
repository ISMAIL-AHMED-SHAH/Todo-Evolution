/**
 * TaskFormModal Component
 *
 * Modal wrapper for task creation and editing forms.
 * Provides slide-in animation with Framer Motion and manages form state.
 * Uses ScrollArea for smooth, accessible scrolling on all screen sizes.
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
import { ScrollArea } from '@/components/ui/scroll-area';
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
      <DialogContent className="w-[calc(100%-1.5rem)] sm:w-[90vw] max-w-[650px] h-[95vh] sm:h-auto sm:max-h-[90vh] p-0 bg-white dark:bg-gray-800 overflow-hidden flex flex-col gap-0">
        <AnimatePresence mode="wait">
          {isOpen && (
            <motion.div
              variants={modalVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="flex flex-col h-full"
            >
              {/* Fixed Header */}
              <DialogHeader className="px-5 sm:px-6 pt-5 sm:pt-6 pb-3 sm:pb-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
                <DialogTitle className="text-lg sm:text-xl md:text-2xl font-bold text-gray-900 dark:text-white pr-8">
                  {mode === 'create' ? 'Create New Task' : 'Edit Task'}
                </DialogTitle>
                <DialogDescription className="text-xs sm:text-sm text-gray-600 dark:text-gray-300 mt-1">
                  {mode === 'create'
                    ? 'Fill out the form below to create a new task. All fields except title are optional.'
                    : 'Update the task details below and click Save Changes.'}
                </DialogDescription>
              </DialogHeader>

              {/* Scrollable Form Content with ScrollArea */}
              <ScrollArea className="flex-1 h-full">
                <div className="px-5 sm:px-6 py-4 sm:py-5">
                  {children}
                </div>
              </ScrollArea>
            </motion.div>
          )}
        </AnimatePresence>
      </DialogContent>
    </Dialog>
  );
}

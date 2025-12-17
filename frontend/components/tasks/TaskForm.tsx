/**
 * TaskForm Component
 *
 * Comprehensive form for creating and editing tasks with React Hook Form.
 * Includes all task fields: title, description, priority, category, and due date.
 * Features validation, error handling, and optimistic UI updates.
 */

'use client';

import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { CalendarIcon } from 'lucide-react';
import { format } from 'date-fns';
import { motion } from 'framer-motion';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Calendar } from '@/components/ui/calendar';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { CategoryInput } from './CategoryInput';
import { createTaskSchema, type CreateTaskFormData } from '@/lib/validations';
import { cn } from '@/lib/utils';
import { useToast } from '@/hooks/use-toast';
import type { Task } from '@/types/task';

interface TaskFormProps {
  mode: 'create' | 'edit';
  task?: Task | null;
  onSubmit: (data: CreateTaskFormData) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

/**
 * Priority badge color mapping
 */
const priorityColors = {
  High: 'bg-red-200 text-red-900 border-red-300',
  Medium: 'bg-orange-200 text-orange-900 border-orange-300',
  Low: 'bg-green-200 text-green-900 border-green-300',
};

/**
 * Form field animation variant
 */
const fieldVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.05,
      type: 'spring' as const,
      stiffness: 300,
      damping: 25,
    },
  }),
};

export function TaskForm({
  mode,
  task,
  onSubmit,
  onCancel,
  isLoading = false,
}: TaskFormProps) {
  const { success, error } = useToast();

  const form = useForm({
    resolver: zodResolver(createTaskSchema),
    defaultValues: {
      title: '',
      description: null,
      priority: 'Medium' as const,
      category: [] as string[],
      due_date: null,
    },
  });

  /**
   * Pre-fill form when editing
   */
  useEffect(() => {
    if (mode === 'edit' && task) {
      form.reset({
        title: task.title,
        description: task.description || '',
        priority: task.priority as 'High' | 'Medium' | 'Low',
        category: task.category || [],
        due_date: task.due_date || undefined,
      });
    }
  }, [mode, task, form]);

  /**
   * Handle form submission with toast notifications (T113)
   * T116: Clear form fields after successful creation
   */
  const handleSubmit = async (data: CreateTaskFormData) => {
    try {
      // Call parent's onSubmit handler
      await onSubmit(data);

      // Show success toast (T113)
      success(
        mode === 'create'
          ? `Task "${data.title}" created successfully!`
          : `Task "${data.title}" updated successfully!`,
        mode === 'create' ? 'Task Created' : 'Task Updated'
      );

      // Reset form to default values after submission (T116 - for create mode)
      // This ensures form is clean for next creation
      if (mode === 'create') {
        form.reset({
          title: '',
          description: null,
          priority: 'Medium',
          category: [],
          due_date: null,
        });
      }
    } catch (err) {
      // Show error toast (T113)
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      error(
        mode === 'create'
          ? `Failed to create task: ${errorMessage}`
          : `Failed to update task: ${errorMessage}`,
        'Error'
      );
    }
  };

  /**
   * Handle form cancellation
   */
  const handleCancel = () => {
    form.reset();
    onCancel();
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        {/* Title Field - Required (T108) */}
        <motion.div
          custom={0}
          variants={fieldVariants}
          initial="hidden"
          animate="visible"
        >
          <FormField
            control={form.control}
            name="title"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-sm font-semibold">
                  Title <span className="text-red-500">*</span>
                </FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="Enter task title..."
                    disabled={isLoading}
                    className="text-base"
                    autoFocus
                  />
                </FormControl>
                <FormDescription className="text-xs text-gray-500">
                  A clear, concise title for your task (required)
                </FormDescription>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </motion.div>

        {/* Description Field - Optional (T109) */}
        <motion.div
          custom={1}
          variants={fieldVariants}
          initial="hidden"
          animate="visible"
        >
          <FormField
            control={form.control}
            name="description"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-sm font-semibold">
                  Description
                </FormLabel>
                <FormControl>
                  <Textarea
                    {...field}
                    placeholder="Add a detailed description (optional)..."
                    disabled={isLoading}
                    rows={4}
                    className="resize-none text-base"
                    value={field.value || ''}
                  />
                </FormControl>
                <FormDescription className="text-xs text-gray-500">
                  Provide additional details about this task
                </FormDescription>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </motion.div>

        {/* Priority Selector - With color indicators (T110) */}
        <motion.div
          custom={2}
          variants={fieldVariants}
          initial="hidden"
          animate="visible"
        >
          <FormField
            control={form.control}
            name="priority"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-sm font-semibold">
                  Priority
                </FormLabel>
                <Select
                  onValueChange={field.onChange}
                  defaultValue={field.value}
                  disabled={isLoading}
                >
                  <FormControl>
                    <SelectTrigger className="text-base">
                      <SelectValue placeholder="Select priority level" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="High">
                      <div className="flex items-center gap-2">
                        <div
                          className={cn(
                            'w-3 h-3 rounded-full border',
                            priorityColors.High
                          )}
                        />
                        <span>High</span>
                      </div>
                    </SelectItem>
                    <SelectItem value="Medium">
                      <div className="flex items-center gap-2">
                        <div
                          className={cn(
                            'w-3 h-3 rounded-full border',
                            priorityColors.Medium
                          )}
                        />
                        <span>Medium</span>
                      </div>
                    </SelectItem>
                    <SelectItem value="Low">
                      <div className="flex items-center gap-2">
                        <div
                          className={cn(
                            'w-3 h-3 rounded-full border',
                            priorityColors.Low
                          )}
                        />
                        <span>Low</span>
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
                <FormDescription className="text-xs text-gray-500">
                  Set the priority level for this task
                </FormDescription>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </motion.div>

        {/* Category/Tags Input (T111) */}
        <motion.div
          custom={3}
          variants={fieldVariants}
          initial="hidden"
          animate="visible"
        >
          <FormField
            control={form.control}
            name="category"
            render={({ field }) => (
              <FormItem>
                <FormLabel className="text-sm font-semibold">
                  Categories
                </FormLabel>
                <FormControl>
                  <CategoryInput
                    value={field.value || []}
                    onChange={field.onChange}
                    disabled={isLoading}
                  />
                </FormControl>
                <FormDescription className="text-xs text-gray-500">
                  Add tags to organize your tasks (max 10)
                </FormDescription>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </motion.div>

        {/* Due Date Picker (T112) */}
        <motion.div
          custom={4}
          variants={fieldVariants}
          initial="hidden"
          animate="visible"
        >
          <FormField
            control={form.control}
            name="due_date"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel className="text-sm font-semibold">
                  Due Date
                </FormLabel>
                <Popover>
                  <PopoverTrigger asChild>
                    <FormControl>
                      <Button
                        variant="outline"
                        className={cn(
                          'w-full pl-3 text-left font-normal text-base',
                          !field.value && 'text-muted-foreground'
                        )}
                        disabled={isLoading}
                      >
                        {field.value ? (
                          format(new Date(field.value), 'PPP')
                        ) : (
                          <span>Pick a due date</span>
                        )}
                        <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                      </Button>
                    </FormControl>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={field.value ? new Date(field.value) : undefined}
                      onSelect={(date) => {
                        field.onChange(
                          date ? format(date, 'yyyy-MM-dd') : undefined
                        );
                      }}
                      disabled={(date) => isLoading}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
                <FormDescription className="text-xs text-gray-500">
                  Optional deadline for this task
                </FormDescription>
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          custom={5}
          variants={fieldVariants}
          initial="hidden"
          animate="visible"
          className="flex flex-col sm:flex-row gap-3 pt-4 border-t"
        >
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full sm:flex-1 bg-teal-600 hover:bg-teal-700 text-white min-h-[44px]"
          >
            {isLoading
              ? mode === 'create'
                ? 'Creating...'
                : 'Saving...'
              : mode === 'create'
              ? 'Create Task'
              : 'Save Changes'}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={handleCancel}
            disabled={isLoading}
            className="w-full sm:flex-1 min-h-[44px]"
          >
            Cancel
          </Button>
        </motion.div>
      </form>
    </Form>
  );
}

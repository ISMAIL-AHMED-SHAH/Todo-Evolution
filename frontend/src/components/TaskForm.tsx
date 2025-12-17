import React, { useState } from 'react';
import { TaskCreate } from '../services/api';
import { validateTaskTitle, validateTaskDescription } from '../utils/validation';

interface TaskFormProps {
  onSubmit: (taskData: TaskCreate) => void;
  onCancel?: () => void;
  initialData?: Partial<TaskCreate>;
}

const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, onCancel, initialData = {} }) => {
  const [title, setTitle] = useState(initialData.title || '');
  const [description, setDescription] = useState(initialData.description || '');
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate inputs
    const titleValidation = validateTaskTitle(title);
    const descriptionValidation = validateTaskDescription(description);

    if (!titleValidation.isValid || !descriptionValidation.isValid) {
      setErrors({
        title: titleValidation.error,
        description: descriptionValidation.error,
      });
      return;
    }

    // Clear errors and submit
    setErrors({});
    onSubmit({
      title: title.trim(),
      description: description.trim() || undefined
    });

    // Reset form
    setTitle('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" aria-label={initialData.title ? "Edit task form" : "Add task form"}>
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title <span aria-label="required">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (errors.title) setErrors({ ...errors, title: undefined });
          }}
          required
          className={`mt-1 block w-full px-4 py-3 sm:py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 text-base sm:text-sm min-h-[44px] ${
            errors.title
              ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
              : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'
          }`}
          placeholder="Enter task title"
          aria-required="true"
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? 'title-error' : undefined}
        />
        {errors.title && (
          <p id="title-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.title}
          </p>
        )}
      </div>
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description <span className="text-gray-500 text-xs">(optional)</span>
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => {
            setDescription(e.target.value);
            if (errors.description) setErrors({ ...errors, description: undefined });
          }}
          rows={3}
          className={`mt-1 block w-full px-4 py-3 sm:py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 text-base sm:text-sm resize-y ${
            errors.description
              ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
              : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500'
          }`}
          placeholder="Add more details about your task"
          aria-label="Task description"
          aria-invalid={!!errors.description}
          aria-describedby={errors.description ? 'description-error' : undefined}
        />
        {errors.description && (
          <p id="description-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.description}
          </p>
        )}
      </div>
      <div className="flex flex-col sm:flex-row gap-3">
        <button
          type="submit"
          className="inline-flex justify-center items-center py-3 sm:py-2 px-4 border border-transparent shadow-sm text-base sm:text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 min-h-[44px] touch-manipulation"
          aria-label={initialData.title ? 'Update task' : 'Add task'}
        >
          {initialData.title ? 'Update Task' : 'Add Task'}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="inline-flex justify-center items-center py-3 sm:py-2 px-4 border border-gray-300 shadow-sm text-base sm:text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 min-h-[44px] touch-manipulation"
            aria-label="Cancel editing"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default TaskForm;
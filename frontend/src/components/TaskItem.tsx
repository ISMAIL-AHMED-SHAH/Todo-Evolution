import React, { useState } from 'react';
import { Task } from '../services/api';

interface TaskItemProps {
  task: Task;
  onToggleCompletion: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onUpdate: (task: Task) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onToggleCompletion,
  onDelete,
  onUpdate
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    // Update the task with new values
    onUpdate({
      ...task,
      title: editTitle.trim(),
      description: editDescription.trim() || undefined
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    // Reset to original values
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete(task.id);
  };

  const handleToggle = () => {
    onToggleCompletion(task);
  };

  return (
    <li className="px-4 py-4 sm:px-6 hover:bg-gray-50 transition-colors duration-150">
      {isEditing ? (
        <div className="space-y-3" role="form" aria-label="Edit task">
          <label htmlFor={`edit-title-${task.id}`} className="sr-only">
            Task title
          </label>
          <input
            id={`edit-title-${task.id}`}
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="block w-full px-4 py-3 sm:py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-base sm:text-sm min-h-[44px]"
            placeholder="Task title"
            aria-required="true"
          />
          <label htmlFor={`edit-description-${task.id}`} className="sr-only">
            Task description
          </label>
          <textarea
            id={`edit-description-${task.id}`}
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            rows={2}
            className="block w-full px-4 py-3 sm:py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-base sm:text-sm resize-y"
            placeholder="Task description (optional)"
            aria-label="Task description"
          />
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-2">
            <button
              onClick={handleSave}
              className="inline-flex justify-center items-center py-3 sm:py-2 px-4 border border-transparent shadow-sm text-base sm:text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 min-h-[44px] touch-manipulation"
              aria-label="Save changes"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="inline-flex justify-center items-center py-3 sm:py-2 px-4 border border-gray-300 shadow-sm text-base sm:text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 min-h-[44px] touch-manipulation"
              aria-label="Cancel editing"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div className="flex items-start sm:items-center flex-1 min-w-0">
              <div className="flex items-center h-11 sm:h-auto">
                <input
                  type="checkbox"
                  id={`task-checkbox-${task.id}`}
                  checked={task.completed}
                  onChange={handleToggle}
                  className="h-5 w-5 sm:h-4 sm:w-4 text-indigo-600 focus:ring-2 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer touch-manipulation"
                  aria-label={task.completed ? `Mark "${task.title}" as incomplete` : `Mark "${task.title}" as complete`}
                />
              </div>
              <label
                htmlFor={`task-checkbox-${task.id}`}
                className={`ml-3 text-base sm:text-sm font-medium cursor-pointer break-words ${
                  task.completed ? 'line-through text-gray-500' : 'text-gray-900'
                }`}
              >
                {task.title}
              </label>
            </div>
            <div className="flex gap-2 sm:gap-3 ml-8 sm:ml-0">
              <button
                onClick={handleEdit}
                className="inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded min-h-[44px] sm:min-h-0 touch-manipulation"
                aria-label={`Edit task: ${task.title}`}
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="inline-flex items-center justify-center px-3 py-2 text-sm font-medium text-red-600 hover:text-red-900 focus:outline-none focus:ring-2 focus:ring-red-500 rounded min-h-[44px] sm:min-h-0 touch-manipulation"
                aria-label={`Delete task: ${task.title}`}
              >
                Delete
              </button>
            </div>
          </div>
          {task.description && (
            <div className="ml-8 mt-2 text-sm text-gray-500 break-words">
              {task.description}
            </div>
          )}
          <div className="ml-8 mt-2 text-xs sm:text-xs text-gray-400">
            <time dateTime={task.created_at}>
              Created: {new Date(task.created_at).toLocaleString()}
            </time>
            {task.updated_at !== task.created_at && (
              <time dateTime={task.updated_at}>
                , Updated: {new Date(task.updated_at).toLocaleString()}
              </time>
            )}
          </div>
        </div>
      )}
    </li>
  );
};

export default TaskItem;
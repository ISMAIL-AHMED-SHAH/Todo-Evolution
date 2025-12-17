import React from 'react';
import { Task } from '../services/api';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onToggleCompletion: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onUpdate: (task: Task) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleCompletion,
  onDelete,
  onUpdate
}) => {
  if (tasks.length === 0) {
    return (
      <div
        className="text-center py-8 bg-white shadow rounded-md"
        role="status"
        aria-label="No tasks available"
      >
        <p className="text-sm sm:text-base text-gray-500">
          No tasks yet. Add one to get started!
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden rounded-md sm:rounded-md">
      <ul
        className="divide-y divide-gray-200"
        role="list"
        aria-label="Task list"
      >
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggleCompletion={onToggleCompletion}
            onDelete={onDelete}
            onUpdate={onUpdate}
          />
        ))}
      </ul>
    </div>
  );
};

export default TaskList;
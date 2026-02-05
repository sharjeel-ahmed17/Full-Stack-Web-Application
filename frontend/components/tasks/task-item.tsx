'use client';

'use client';

import React, { useState } from 'react';
import { Task } from '@/types';
import { apiClient } from '@/lib/api';
import { Edit3, Trash2, CheckCircle, Circle } from 'lucide-react';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onToggle: (task: Task) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onEdit, onDelete, onToggle }) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      const response = await apiClient.toggleTaskCompletion(task.id);
      onToggle({
        ...task,
        is_completed: response.is_completed,
        updated_at: response.updated_at
      });
    } catch (err) {
      console.error('Failed to toggle task:', err);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await apiClient.deleteTask(task.id);
      onDelete(task.id);
    } catch (err) {
      console.error('Failed to delete task:', err);
      setIsDeleting(false);
    }
  };

  return (
    <div className={`flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow duration-200 ${task.is_completed ? 'opacity-75' : ''}`}>
      <div className="flex items-center mr-4">
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className="flex items-center justify-center w-6 h-6 rounded-full border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:ring-offset-2 transition-colors"
          aria-label={task.is_completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.is_completed ? (
            <CheckCircle className="w-4 h-4 text-green-500" />
          ) : (
            <Circle className="w-4 h-4 text-gray-400 dark:text-gray-500" />
          )}
        </button>
      </div>

      <div className="flex-1 min-w-0">
        <h3 className={`text-lg font-medium truncate ${task.is_completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-900 dark:text-white'}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className={`text-sm truncate ${task.is_completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-600 dark:text-gray-300'}`}>
            {task.description}
          </p>
        )}
        <div className="flex items-center mt-1 text-xs text-gray-500 dark:text-gray-400">
          <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
          {task.updated_at && task.updated_at !== task.created_at && (
            <span className="ml-2">Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
          )}
        </div>
      </div>

      <div className="flex space-x-2 ml-4">
        <button
          onClick={() => onEdit(task)}
          className="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors duration-200"
          aria-label="Edit task"
        >
          <Edit3 className="w-4 h-4" />
        </button>
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="p-2 text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors duration-200"
          aria-label="Delete task"
        >
          {isDeleting ? (
            <span className="text-xs">Deleting...</span>
          ) : (
            <Trash2 className="w-4 h-4" />
          )}
        </button>
      </div>
    </div>
  );
};

export default TaskItem;
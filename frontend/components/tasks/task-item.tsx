'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Task } from '@/types';
import { apiClient } from '@/lib/api';

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
    <div className={`flex items-center p-4 border rounded-lg ${task.is_completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex items-center mr-4">
        <Checkbox
          checked={task.is_completed}
          onCheckedChange={handleToggle}
          disabled={isToggling}
          className="mr-2"
        />
      </div>

      <div className="flex-1 min-w-0">
        <h3 className={`text-lg font-medium truncate ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className={`text-sm truncate ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-500'}`}>
            {task.description}
          </p>
        )}
      </div>

      <div className="flex space-x-2 ml-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(task)}
        >
          Edit
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={handleDelete}
          disabled={isDeleting}
        >
          {isDeleting ? 'Deleting...' : 'Delete'}
        </Button>
      </div>
    </div>
  );
};

export default TaskItem;
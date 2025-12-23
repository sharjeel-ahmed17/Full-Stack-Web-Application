'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Task, TaskCreateRequest, TaskUpdateRequest } from '@/types';
import { apiClient } from '@/lib/api';

interface TaskFormProps {
  task?: Task;
  onSubmit: (task: Task) => void;
  onCancel: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let updatedTask: Task;

      if (task) {
        // Update existing task
        const updateData: TaskUpdateRequest = {
          title: title.trim(),
          description: description.trim() || undefined
        };
        updatedTask = await apiClient.updateTask(task.id, updateData);
      } else {
        // Create new task
        const createData: TaskCreateRequest = {
          title: title.trim(),
          description: description.trim() || undefined
        };
        updatedTask = await apiClient.createTask(createData);
      }

      onSubmit(updatedTask);
    } catch (err: any) {
      setError(err.message || 'Failed to save task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg bg-gray-50">
      {error && (
        <div className="p-3 text-sm text-red-700 bg-red-100 rounded-md">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title
        </label>
        <Input
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="mt-1"
          placeholder="Task title"
          disabled={loading}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
          rows={3}
          placeholder="Task description (optional)"
          disabled={loading}
        />
      </div>

      <div className="flex justify-end space-x-2">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={loading}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={loading}
        >
          {loading ? (task ? 'Updating...' : 'Creating...') : (task ? 'Update Task' : 'Create Task')}
        </Button>
      </div>
    </form>
  );
};

export default TaskForm;
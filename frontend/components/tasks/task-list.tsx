'use client';

'use client';

import React, { useState, useEffect } from 'react';
import { Task } from '@/types';
import { apiClient } from '@/lib/api';
import TaskItem from '@/components/tasks/task-item';
import EmptyState from '@/components/tasks/empty-state';
import TaskForm from '@/components/tasks/task-form';
import { Plus, RotateCcw } from 'lucide-react';

const TaskList = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getTasks();
      setTasks(response.tasks);
    } catch (err: any) {
      // Check if it's an authentication error
      if (err.message && (err.message.includes('Authentication failed') || err.message.includes('Not authenticated') || err.message.includes('401') || err.message.includes('403'))) {
        setError('You need to log in first. Redirecting to login...');
        // Redirect to login after a short delay
        setTimeout(() => {
          if (typeof window !== 'undefined') {
            // Preserve the current location for redirect after login
            const currentUrl = window.location.href;
            window.location.href = `/login?redirect=${encodeURIComponent(currentUrl)}`;
          }
        }, 2000);
      } else {
        setError(err.message || 'Failed to load tasks');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = (task: Task) => {
    setTasks([task, ...tasks]);
    setShowCreateForm(false);
  };

  const handleUpdateTask = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
    setEditingTask(null);
  };

  const handleDeleteTask = (taskId: string) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleToggleTask = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 dark:border-blue-400"></div>
        <p className="mt-4 text-gray-600 dark:text-gray-300">Loading your tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-700 bg-red-50 dark:bg-red-900/20 rounded-xl border border-red-200 dark:border-red-800">
        <div className="flex items-center">
          <span className="font-medium">Error:</span>
          <span className="ml-2">{error}</span>
        </div>
        <button
          onClick={fetchTasks}
          className="mt-4 inline-flex items-center px-4 py-2 bg-red-100 dark:bg-red-800/30 text-red-700 dark:text-red-300 rounded-lg hover:bg-red-200 dark:hover:bg-red-800/50 transition-colors duration-200"
        >
          <RotateCcw className="w-4 h-4 mr-2" />
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {showCreateForm ? (
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowCreateForm(false)}
        />
      ) : (
        <div className="flex justify-end">
          <button
            onClick={() => setShowCreateForm(true)}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 transition-colors duration-200 shadow-md hover:shadow-lg"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create New Task
          </button>
        </div>
      )}

      {editingTask && (
        <TaskForm
          task={editingTask}
          onSubmit={handleUpdateTask}
          onCancel={() => setEditingTask(null)}
        />
      )}

      {tasks.length === 0 ? (
        <EmptyState onCreateTask={() => setShowCreateForm(true)} />
      ) : (
        <div className="space-y-4">
          {tasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onEdit={setEditingTask}
              onDelete={handleDeleteTask}
              onToggle={handleToggleTask}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;
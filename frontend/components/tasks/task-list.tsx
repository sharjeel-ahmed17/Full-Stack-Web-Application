'use client';

import React, { useState, useEffect } from 'react';
import { Task } from '@/types';
import { apiClient } from '@/lib/api';
import TaskItem from '@/components/tasks/task-item';
import EmptyState from '@/components/tasks/empty-state';
import TaskForm from '@/components/tasks/task-form';

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
      setError(err.message || 'Failed to load tasks');
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
    return <div className="text-center py-8">Loading tasks...</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-red-700 bg-red-100 rounded-md">
        Error: {error}
        <button
          onClick={fetchTasks}
          className="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {showCreateForm ? (
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowCreateForm(false)}
        />
      ) : (
        <div className="flex justify-end">
          <button
            onClick={() => setShowCreateForm(true)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
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
        <div className="space-y-3">
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
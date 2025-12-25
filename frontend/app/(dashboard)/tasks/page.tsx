import React from 'react';
import TaskList from '@/components/tasks/task-list';

export default function TasksPage() {
  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
        <p className="mt-1 text-sm text-gray-500">
          Manage your tasks efficiently
        </p>
      </div>

      <TaskList />
    </div>
  );
}
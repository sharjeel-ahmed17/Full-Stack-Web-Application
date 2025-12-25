import React from 'react';
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  onCreateTask?: () => void;
}

const EmptyState: React.FC<EmptyStateProps> = ({ onCreateTask }) => {
  return (
    <div className="text-center py-12">
      <div className="mx-auto h-24 w-24 text-gray-400">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
      </div>
      <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks</h3>
      <p className="mt-1 text-sm text-gray-500">
        Get started by creating a new task.
      </p>
      {onCreateTask && (
        <div className="mt-6">
          <Button onClick={onCreateTask}>
            Create your first task
          </Button>
        </div>
      )}
    </div>
  );
};

export default EmptyState;
import React, { useEffect } from 'react';

interface TaskConfirmationProps {
  isVisible: boolean;
  message: string;
  type: 'success' | 'info' | 'warning' | 'error';
  duration?: number;
  onClose: () => void;
}

const TaskConfirmation: React.FC<TaskConfirmationProps> = ({
  isVisible,
  message,
  type,
  duration = 5000,
  onClose
}) => {
  // Auto close after duration
  useEffect(() => {
    if (isVisible && duration > 0) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [isVisible, duration, onClose]);

  if (!isVisible) {
    return null;
  }

  const bgColor = {
    success: 'bg-green-100 border-green-400 text-green-700',
    info: 'bg-blue-100 border-blue-400 text-blue-700',
    warning: 'bg-yellow-100 border-yellow-400 text-yellow-700',
    error: 'bg-red-100 border-red-400 text-red-700',
  }[type];

  const icon = {
    success: '✓',
    info: 'ℹ',
    warning: '⚠',
    error: '✗',
  }[type];

  return (
    <div
      className={`border rounded-lg p-4 mb-4 ${bgColor}`}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-start">
        <span className="mr-2 font-bold text-lg" aria-hidden="true">{icon}</span>
        <div className="flex-1">
          <p>{message}</p>
        </div>
        <button
          onClick={onClose}
          className="ml-2 text-current hover:opacity-70 focus:outline-none focus:ring-2 focus:ring-offset-2"
          aria-label="Close notification"
        >
          ×
        </button>
      </div>
    </div>
  );
};

export default TaskConfirmation;
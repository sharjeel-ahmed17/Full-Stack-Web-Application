'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ClipboardList, Plus } from 'lucide-react';

interface EmptyStateProps {
  onCreateTask?: () => void;
}

const EmptyState: React.FC<EmptyStateProps> = ({ onCreateTask }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center py-16"
    >
      <motion.div
        className="mx-auto w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mb-6"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
      >
        <ClipboardList className="w-12 h-12 text-blue-600" />
      </motion.div>

      <motion.h3
        className="text-2xl font-bold text-gray-900 mb-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        No tasks yet
      </motion.h3>

      <motion.p
        className="text-gray-600 max-w-md mx-auto mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        Get started by creating your first task. Organize your work and boost your productivity today.
      </motion.p>

      {onCreateTask && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <button
            onClick={onCreateTask}
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 shadow-md hover:shadow-lg"
          >
            <Plus className="w-5 h-5 mr-2" />
            Create your first task
          </button>
        </motion.div>
      )}
    </motion.div>
  );
};

export default EmptyState;
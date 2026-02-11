/**
 * Error handling utilities for chat operations
 */

export interface ChatError {
  type: 'network' | 'authentication' | 'validation' | 'server' | 'unknown';
  message: string;
  code?: string;
  status?: number;
  originalError?: Error;
}

/**
 * Create a standardized error from various error sources
 */
export const createChatError = (error: any, context: string = 'Chat operation'): ChatError => {
  // Handle fetch/network errors
  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    return {
      type: 'network',
      message: `${context}: Network error occurred. Please check your connection.`,
      originalError: error
    };
  }

  // Handle HTTP status errors
  if (error.status) {
    if (error.status === 401 || error.status === 403) {
      return {
        type: 'authentication',
        message: `${context}: Authentication failed. Please log in again.`,
        status: error.status,
        originalError: error
      };
    } else if (error.status >= 400 && error.status < 500) {
      return {
        type: 'validation',
        message: `${context}: Request validation failed (${error.status}).`,
        status: error.status,
        originalError: error
      };
    } else if (error.status >= 500) {
      return {
        type: 'server',
        message: `${context}: Server error (${error.status}). Please try again later.`,
        status: error.status,
        originalError: error
      };
    }
  }

  // Handle string errors
  if (typeof error === 'string') {
    return {
      type: 'unknown',
      message: `${context}: ${error}`
    };
  }

  // Handle Error objects
  if (error instanceof Error) {
    return {
      type: 'unknown',
      message: `${context}: ${error.message}`,
      originalError: error
    };
  }

  // Fallback for unknown error types
  return {
    type: 'unknown',
    message: `${context}: An unknown error occurred.`
  };
};

/**
 * Log error with context
 */
export const logChatError = (error: ChatError, additionalInfo?: Record<string, any>) => {
  console.error('[Chat Error]', {
    type: error.type,
    message: error.message,
    status: error.status,
    code: error.code,
    additionalInfo: additionalInfo || {},
    timestamp: new Date().toISOString()
  });
};

/**
 * Format error message for user display
 */
export const formatUserErrorMessage = (error: ChatError): string => {
  switch (error.type) {
    case 'network':
      return 'Network connection issue. Please check your internet connection and try again.';
    case 'authentication':
      return 'Session expired. Please log in again to continue.';
    case 'validation':
      return 'Invalid input provided. Please check your message and try again.';
    case 'server':
      return 'Service temporarily unavailable. Please try again later.';
    default:
      return error.message || 'An unexpected error occurred. Please try again.';
  }
};

/**
 * Check if error is retryable
 */
export const isRetryableError = (error: ChatError): boolean => {
  return error.type === 'network' || error.type === 'server';
};
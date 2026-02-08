/**
 * Authentication helper to retrieve JWT token for chat requests
 */
import { apiClient } from '@/lib/api';

/**
 * Get the JWT token from the current session
 */
export const getAuthToken = (): string | null => {
  // Use the existing token management from api.ts
  if (typeof window !== 'undefined') {
    // First try localStorage
    let token = localStorage.getItem('access_token');

    // If not in localStorage, try to get from cookie
    if (!token) {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'access_token') {
          token = value;
          break;
        }
      }
    }

    return token;
  }
  return null;
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  return !!token;
};

/**
 * Get the current user ID
 */
export const getCurrentUserId = async (): Promise<string> => {
  try {
    // Get current user info from the existing API client
    const user = await apiClient.getCurrentUser();
    return user.id;
  } catch (error) {
    console.error('Failed to get user ID:', error);
    throw new Error('Unable to retrieve user information. Please log in again.');
  }
};
import { Task, User, UserRegisterRequest, UserLoginRequest, TaskCreateRequest, TaskUpdateRequest, LogoutResponse } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Helper function to manage authentication tokens in both localStorage and cookies
function getToken(): string | null {
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
}

function setToken(token: string): void {
  if (typeof window !== 'undefined') {
    // Store in both localStorage and cookie
    localStorage.setItem('access_token', token);
    // Set cookie with SameSite attribute for security
    document.cookie = `access_token=${token}; path=/; SameSite=Lax;`;
  }
}

function removeToken(): void {
  if (typeof window !== 'undefined') {
    // Remove from both localStorage and cookie
    localStorage.removeItem('access_token');
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
  }
}

// Helper function to determine the appropriate protocol for API requests
function getSecureApiUrl(): string {
  // Check if we're in a browser environment
  if (typeof window !== 'undefined') {
    // For deployment scenarios, we need to ensure consistency
    // If API_BASE_URL is configured for a remote server, use as-is
    // Don't modify the configured URL as it should be properly set for the deployment
    return API_BASE_URL;
  }
  return API_BASE_URL;
}

class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${getSecureApiUrl()}${endpoint}`;

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      credentials: 'include', // Include credentials (cookies, etc.) for CORS requests
      mode: 'cors', // Explicitly set CORS mode
      ...options,
    };

    // Include token if available (only in browser environment)
    if (typeof window !== 'undefined') {
      const token = getToken();
      if (token) {
        (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
      }
    }

    // Log for debugging (will be removed in production)
    if (typeof window !== 'undefined') {
      console.log('Making API request to:', url);
      console.log('Token available:', !!localStorage.getItem('access_token'));
      console.log('Headers:', config.headers);
    }

    let response;
    try {
      response = await fetch(url, config);
    } catch (error) {
      console.error('Network error during API request:', error);

      // Handle redirect errors specifically
      if (error instanceof TypeError && error.message.includes('redirect')) {
        throw new Error('CORS error: The server is redirecting requests in a way that violates CORS policy. Please contact the backend administrator.');
      }

      throw error;
    }

    // Check for authentication errors specifically
    if (response.status === 401 || response.status === 403) {
      const errorText = await response.text().catch(() => 'Unauthorized');
      console.error('Authentication error:', errorText);

      // Optionally redirect to login if unauthenticated
      if (typeof window !== 'undefined') {
        // Remove invalid token if present
        localStorage.removeItem('access_token');
        // You could optionally redirect to login here
        // window.location.href = '/login';
      }

      throw new Error('Authentication failed: ' + errorText);
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Auth endpoints
  async register(userData: UserRegisterRequest): Promise<User> {
    return this.request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(userData: UserLoginRequest): Promise<{ access_token: string; token_type: string }> {
    const formData = new URLSearchParams();
    formData.append('username', userData.email);
    formData.append('password', userData.password);

    const response = await this.request('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    // Store the token in both localStorage and cookie
    if (typeof window !== 'undefined' && response.access_token) {
      setToken(response.access_token);
    }

    return response;
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/auth/me');
  }

  // Task endpoints
  async getTasks(): Promise<{ tasks: Task[]; total: number }> {
    return this.request('/tasks');
  }

  async createTask(taskData: TaskCreateRequest): Promise<Task> {
    return this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(taskId: string, taskData: TaskUpdateRequest): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId: string): Promise<void> {
    await this.request(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: string): Promise<{ id: string; is_completed: boolean; updated_at: string }> {
    return this.request(`/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }

  // Logout endpoint
  async logout(): Promise<LogoutResponse> {
    const response = await this.request<LogoutResponse>('/auth/logout', {
      method: 'POST',
    });

    // Remove token from storage after successful logout
    if (typeof window !== 'undefined') {
      removeToken();
    }

    return response;
  }
}

export const apiClient = new ApiClient();
export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  user_id: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
}

export interface TaskToggleResponse {
  id: string;
  is_completed: boolean;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface UserRegisterRequest {
  email: string;
  password: string;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}
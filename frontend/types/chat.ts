/**
 * TypeScript definitions for chat-related data structures
 */

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  status: 'sending' | 'sent' | 'received' | 'error';
  toolCalls?: Array<any>;
}

export interface ConversationState {
  id?: string;
  messages: Message[];
  isLoading: boolean;
  error?: string;
  userId: string;
  lastUpdated: Date;
}

export interface ChatRequest {
  message: string;
  metadata?: Record<string, any>;
}

export interface ChatResponse {
  conversation_id: string;
  response: {
    content: string;
    role: string;
  };
  tool_calls: Array<any>;
  timestamp: string;
}

export interface UIState {
  inputValue: string;
  isConnected: boolean;
  connectionError?: string;
  showTaskConfirmation?: boolean;
}

export interface TaskConfirmation {
  isVisible: boolean;
  message: string;
  type: 'success' | 'info' | 'warning';
  duration?: number;
}

export interface ChatAPIClientConfig {
  baseUrl: string;
  authToken: string;
  userId: string;
  timeout: number;
}

export interface APIError {
  code: string;
  message: string;
  status: number;
  timestamp: Date;
}

export interface ClientError {
  type: string;
  message: string;
  component: string;
  timestamp: Date;
}
import { ChatRequest, ChatResponse } from '@/types/chat';

/**
 * API client functions for chat endpoint integration
 */
class ChatAPIClient {
  private baseUrl: string;
  private authToken: string;

  constructor(config: { baseUrl: string; authToken: string }) {
    this.baseUrl = config.baseUrl;
    this.authToken = config.authToken;
  }

  /**
   * Send a message to the chat endpoint
   */
  async sendMessage(userId: string, messageData: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/v1/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.authToken}`,
      },
      body: JSON.stringify(messageData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Chat API error: ${response.status} - ${errorData.message || 'Unknown error'}`);
    }

    return response.json();
  }

  /**
   * Get conversation history
   */
  async getConversationHistory(userId: string, conversationId: string): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/v1/${userId}/conversations/${conversationId}/messages`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${this.authToken}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Get conversation error: ${response.status} - ${errorData.message || 'Unknown error'}`);
    }

    return response.json();
  }

  /**
   * Get user conversations
   */
  async getUserConversations(userId: string): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/v1/${userId}/conversations`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${this.authToken}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`Get user conversations error: ${response.status} - ${errorData.message || 'Unknown error'}`);
    }

    return response.json();
  }
}

export default ChatAPIClient;
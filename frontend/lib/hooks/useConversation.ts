'use client';

import { useState, useEffect, useCallback } from 'react';
import { ConversationState, Message } from '@/types/chat';
import ChatAPIClient from '@/lib/api/chat';
import { getAuthToken, getCurrentUserId } from '@/lib/api/auth';

/**
 * Hook for managing conversation state
 */
export const useConversation = (apiBaseUrl: string) => {
  // Initialize conversation state from local storage if available
  const initializeConversationState = (): ConversationState => {
    const savedState = typeof window !== 'undefined' ? localStorage.getItem('chat-conversation-state') : null;

    if (savedState) {
      try {
        const parsed = JSON.parse(savedState);
        return {
          ...parsed,
          lastUpdated: new Date(parsed.lastUpdated),
          messages: parsed.messages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }))
        };
      } catch (e) {
        console.warn('Failed to parse conversation state from localStorage, using default state');
      }
    }

    return {
      messages: [],
      isLoading: false,
      userId: '',
      lastUpdated: new Date(),
    };
  };

  const [conversation, setConversation] = useState<ConversationState>(() => initializeConversationState());
  const [error, setError] = useState<string | null>(null);

  // Persist conversation state to local storage whenever it changes
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('chat-conversation-state', JSON.stringify(conversation));
    }
  }, [conversation]);

  // Initialize user ID
  useEffect(() => {
    const initializeUserId = async () => {
      try {
        const userId = await getCurrentUserId();
        setConversation(prev => ({
          ...prev,
          userId
        }));
      } catch (err) {
        setError('Failed to initialize user session');
        console.error('Error initializing user ID:', err);
      }
    };

    initializeUserId();
  }, []);

  const sendMessage = useCallback(async (messageContent: string) => {
    if (!conversation.userId) {
      setError('User not authenticated');
      return;
    }

    const authToken = getAuthToken();
    if (!authToken) {
      setError('Authentication token not available');
      return;
    }

    const client = new ChatAPIClient({
      baseUrl: apiBaseUrl,
      authToken: authToken,
    });

    // Add user message to state immediately
    const userMessage: Message = {
      id: Date.now().toString(), // temporary ID until response
      content: messageContent,
      role: 'user',
      timestamp: new Date(),
      status: 'sending'
    };

    setConversation(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true
    }));

    try {
      const response = await client.sendMessage(conversation.userId, {
        message: messageContent,
        metadata: {}
      });

      // Update user message status to sent
      setConversation(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id === userMessage.id ? { ...msg, status: 'sent' } : msg
        ),
        isLoading: false
      }));

      // Add AI response to state
      const role = response.response.role === 'user' ? 'user' : 'assistant';
      const aiMessage: Message = {
        id: response.conversation_id,
        content: response.response.content,
        role: role,
        timestamp: new Date(response.timestamp),
        status: 'received',
        toolCalls: response.tool_calls
      };

      setConversation(prev => ({
        ...prev,
        id: response.conversation_id,
        messages: [...prev.messages, aiMessage],
        lastUpdated: new Date()
      }));

      setError(null);
    } catch (err) {
      console.error('Error sending message:', err);

      // Update user message status to error
      setConversation(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id === userMessage.id ? { ...msg, status: 'error' } : msg
        ),
        isLoading: false
      }));

      setError(`Failed to send message: ${(err as Error).message}`);
    }
  }, [conversation.userId, apiBaseUrl]);

  const loadConversationHistory = useCallback(async (conversationId: string) => {
    if (!conversation.userId) {
      setError('User not authenticated');
      return;
    }

    const authToken = getAuthToken();
    if (!authToken) {
      setError('Authentication token not available');
      return;
    }

    const client = new ChatAPIClient({
      baseUrl: apiBaseUrl,
      authToken: authToken,
    });

    setConversation(prev => ({ ...prev, isLoading: true }));

    try {
      const history = await client.getConversationHistory(conversation.userId, conversationId);

      const messages: Message[] = history.map((msg: any) => ({
        id: msg.id,
        content: msg.content,
        role: msg.role,
        timestamp: new Date(msg.timestamp),
        status: 'received' // Historical messages are already received
      }));

      setConversation(prev => ({
        ...prev,
        id: conversationId,
        messages,
        isLoading: false,
        lastUpdated: new Date()
      }));

      setError(null);
    } catch (err) {
      console.error('Error loading conversation history:', err);
      setConversation(prev => ({ ...prev, isLoading: false }));
      setError(`Failed to load conversation history: ${(err as Error).message}`);
    }
  }, [conversation.userId, apiBaseUrl]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    conversation,
    sendMessage,
    loadConversationHistory,
    error,
    clearError,
    isLoading: conversation.isLoading
  };
};
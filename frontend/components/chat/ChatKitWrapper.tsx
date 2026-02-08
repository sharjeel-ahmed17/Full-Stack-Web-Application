'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useConversation } from '@/lib/hooks/useConversation';
import TaskConfirmation from './TaskConfirmation';

interface ChatKitWrapperProps {
  userId: string;
  apiBaseUrl: string;
}

const ChatKitWrapper: React.FC<ChatKitWrapperProps> = ({ userId, apiBaseUrl }) => {
  const [inputValue, setInputValue] = useState('');
  const [hasMoreMessages, setHasMoreMessages] = useState(true);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [taskConfirmation, setTaskConfirmation] = useState({
    isVisible: false,
    message: '',
    type: 'info' as 'success' | 'info' | 'warning' | 'error',
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesStartRef = useRef<HTMLDivElement>(null);

  const {
    conversation,
    sendMessage,
    loadConversationHistory,
    error,
    clearError,
    isLoading
  } = useConversation(apiBaseUrl);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [conversation.messages]);

  // Handle tool call notifications from messages
  useEffect(() => {
    // Check for new messages with tool calls and show confirmation
    if (conversation.messages.length > 0) {
      const lastMessage = conversation.messages[conversation.messages.length - 1];
      if (lastMessage.toolCalls && lastMessage.toolCalls.length > 0) {
        // Show a confirmation that a tool call was processed
        setTaskConfirmation({
          isVisible: true,
          message: 'Processing your request...',
          type: 'info'
        });

        // After a short delay, update the message to show completion
        setTimeout(() => {
          setTaskConfirmation({
            isVisible: true,
            message: 'Request processed successfully',
            type: 'success'
          });
        }, 1000);
      }
    }
  }, [conversation.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const scrollToTop = () => {
    messagesStartRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle scroll for loading more history
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const element = e.currentTarget;
    if (element.scrollTop === 0 && hasMoreMessages && !isLoadingHistory) {
      // User has scrolled to top, potentially load more history
      // For now, we'll just show a button to load more
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const trimmedValue = inputValue.trim();

    // Validate message content (1-2000 characters)
    if (!trimmedValue) return;
    if (trimmedValue.length < 1) {
      setTaskConfirmation({
        isVisible: true,
        message: 'Message must not be empty',
        type: 'error'
      });
      return;
    }
    if (trimmedValue.length > 2000) {
      setTaskConfirmation({
        isVisible: true,
        message: 'Message exceeds maximum length of 2000 characters',
        type: 'error'
      });
      return;
    }

    // Sanitize the input (basic sanitization)
    const sanitizedValue = trimmedValue.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

    setInputValue('');

    // Show initial task confirmation
    setTaskConfirmation({
      isVisible: true,
      message: 'Sending your message...',
      type: 'info'
    });

    try {
      await sendMessage(sanitizedValue);

      // After successful send, update confirmation
      setTaskConfirmation({
        isVisible: true,
        message: 'Message sent, awaiting response...',
        type: 'info'
      });
    } catch (err) {
      console.error('Failed to send message:', err);
      setTaskConfirmation({
        isVisible: true,
        message: 'Failed to send message',
        type: 'error'
      });
    }
  };

  // Function to load more history (placeholder implementation)
  const loadMoreHistory = async () => {
    if (!hasMoreMessages || isLoadingHistory || !conversation.id) return;

    setIsLoadingHistory(true);
    try {
      // In a full implementation, this would load more messages from the backend
      // based on pagination/infinite scroll logic
      console.log('Loading more history...');
      // This would call loadConversationHistory with appropriate parameters
    } catch (err) {
      console.error('Failed to load more history:', err);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const handleCloseConfirmation = () => {
    setTaskConfirmation(prev => ({ ...prev, isVisible: false }));
  };

  return (
    <div className="flex flex-col h-full min-h-[500px]">
      {/* Task Confirmation */}
      <TaskConfirmation
        isVisible={taskConfirmation.isVisible}
        message={taskConfirmation.message}
        type={taskConfirmation.type}
        onClose={handleCloseConfirmation}
      />

      {/* Error display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <span className="block sm:inline">{error}</span>
          <button
            onClick={clearError}
            className="float-right text-red-700 hover:text-red-900"
          >
            ×
          </button>
        </div>
      )}

      {/* Conversation messages */}
      <div
        className="flex-grow overflow-y-auto mb-4 max-h-[60vh] bg-white border border-gray-200 rounded-lg p-4"
        onScroll={handleScroll}
      >
        {/* Load more button at top if available */}
        {hasMoreMessages && (
          <div className="flex justify-center mb-4">
            <button
              onClick={loadMoreHistory}
              disabled={isLoadingHistory}
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded disabled:opacity-50"
            >
              {isLoadingHistory ? 'Loading...' : 'Load earlier messages'}
            </button>
          </div>
        )}

        <div ref={messagesStartRef} />

        {conversation.messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p className="text-center">Start a conversation by sending a message!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {conversation.messages.map((message) => (
              <div
                key={message.id}
                className={`p-3 rounded-lg max-w-[80%] ${
                  message.role === 'user'
                    ? 'bg-blue-100 ml-auto self-end'
                    : 'bg-gray-100 mr-auto self-start'
                }`}
              >
                <div className="font-medium text-sm mb-1">
                  {message.role === 'user' ? 'You' : 'AI Assistant'}
                </div>
                <div className="text-gray-800">{message.content}</div>
                {message.status === 'sending' && (
                  <div className="text-xs text-gray-500 mt-1">Sending...</div>
                )}
                {message.status === 'error' && (
                  <div className="text-xs text-red-500 mt-1">Error sending message</div>
                )}

                {/* Display tool call information if present */}
                {message.toolCalls && message.toolCalls.length > 0 && (
                  <div className="mt-2 p-2 bg-blue-50 rounded text-xs text-blue-600">
                    {message.toolCalls.length} tool call(s) executed
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 p-3 rounded-lg mr-auto">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form onSubmit={handleSubmit} className="mt-auto" role="form" aria-label="Chat message form">
        <div className="flex gap-2">
          <input
            type="text"
            id="chat-input"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
            aria-label="Type your message"
            aria-describedby="send-button"
          />
          <button
            type="submit"
            id="send-button"
            disabled={isLoading || !inputValue.trim()}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label={isLoading ? "Sending message" : "Send message"}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatKitWrapper;
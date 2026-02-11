'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import Chatbot from '@/components/chatbot/Chatbot';

interface ChatbotContextType {
  showChatbot: boolean;
  setShowChatbot: React.Dispatch<React.SetAction<boolean>>;
}

const ChatbotContext = createContext<ChatbotContextType | undefined>(undefined);

export const useChatbot = () => {
  const context = useContext(ChatbotContext);
  if (!context) {
    throw new Error('useChatbot must be used within a ChatbotProvider');
  }
  return context;
};

export const ChatbotProvider = ({ children }: { children: React.ReactNode }) => {
  const [showChatbot, setShowChatbot] = useState(false);
  const pathname = usePathname();

  // Determine if user is logged in based on route and token presence
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    
    // Show chatbot only on protected routes when user is logged in
    // Protected routes are defined in middleware as ['/tasks', '/dashboard']
    const isProtectedRoute = pathname.startsWith('/tasks') || pathname.startsWith('/dashboard');
    const hasToken = !!token;
    
    if (isProtectedRoute && hasToken) {
      setShowChatbot(true);
    } else {
      setShowChatbot(false);
    }
  }, [pathname]);

  return (
    <ChatbotContext.Provider value={{ showChatbot, setShowChatbot }}>
      {children}
      {showChatbot && <Chatbot />}
    </ChatbotContext.Provider>
  );
};
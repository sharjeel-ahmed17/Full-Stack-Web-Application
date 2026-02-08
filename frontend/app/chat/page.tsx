'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatKitWrapper from '@/components/chat/ChatKitWrapper';
import { getCurrentUserId } from '@/lib/api/auth';

const ChatPage = () => {
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

  useEffect(() => {
    const loadUser = async () => {
      try {
        const currentUserId = await getCurrentUserId();
        setUserId(currentUserId);
      } catch (err) {
        console.error('Error getting user ID:', err);
        setError('Failed to load user session. Please log in again.');
        // Redirect to login after a short delay
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading chat...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-red-500 text-xl">{error}</div>
      </div>
    );
  }

  if (!userId) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">User not authenticated</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6 text-center">AI Chat Assistant</h1>
      <div
        className="border border-gray-200 rounded-lg p-4 h-[600px] flex flex-col"
        role="main"
        aria-label="Chat interface"
      >
        <ChatKitWrapper userId={userId} apiBaseUrl={`${apiBaseUrl}/v1`} />
      </div>
    </div>
  );
};

export default ChatPage;
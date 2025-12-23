'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { UserLoginRequest } from '@/types';
import { apiClient } from '@/lib/api';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const userData: UserLoginRequest = { email, password };
      const response = await apiClient.login(userData);

      // Store the token in localStorage
      localStorage.setItem('access_token', response.access_token);

      // Redirect to dashboard after successful login
      router.push('/tasks');
      router.refresh();
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
      <div className="text-center">
        <h2 className="text-3xl font-bold">Sign In</h2>
        <p className="mt-2 text-gray-600">Enter your credentials to continue</p>
      </div>

      {error && (
        <div className="p-3 text-sm text-red-700 bg-red-100 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email
          </label>
          <Input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="mt-1"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Password
          </label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="mt-1"
            placeholder="••••••••"
          />
        </div>

        <Button
          type="submit"
          className="w-full"
          disabled={loading}
        >
          {loading ? 'Signing In...' : 'Sign In'}
        </Button>
      </form>

      <div className="text-center text-sm text-gray-600">
        Don't have an account?{' '}
        <a href="/register" className="font-medium text-blue-600 hover:text-blue-500">
          Sign up
        </a>
      </div>
    </div>
  );
};

export default LoginForm;
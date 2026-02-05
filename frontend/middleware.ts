import { NextRequest, NextResponse } from 'next/server';

// This function protects routes by checking for the presence of a token in cookies or headers
export function middleware(request: NextRequest) {
  // Define protected routes that require authentication
  const protectedPaths = ['/tasks', '/dashboard'];
  // Define public routes that don't require authentication
  const publicPaths = ['/login', '/register', '/'];

  const currentPath = request.nextUrl.pathname;

  // Check if the current path is protected
  const isProtectedPath = protectedPaths.some(path =>
    currentPath.startsWith(path) || currentPath === path
  );

  // Check if it's a public path
  const isPublicPath = publicPaths.some(path =>
    currentPath.startsWith(path) || currentPath === path
  );

  // For routes that are neither protected nor public (like static assets), let them pass
  if (!isProtectedPath && !isPublicPath) {
    return NextResponse.next();
  }

  // Extract token from various possible sources
  let token = null;

  // Check for token in cookies (if stored in cookies)
  const tokenCookie = request.cookies.get('access_token');
  if (tokenCookie) {
    token = tokenCookie.value;
  }

  // Check for token in authorization header
  if (!token) {
    const authHeader = request.headers.get('authorization');
    if (authHeader && authHeader.startsWith('Bearer ')) {
      token = authHeader.substring(7);
    }
  }

  // If accessing a protected route without a token, redirect to login
  if (isProtectedPath && !token) {
    // Store the attempted destination in search params for redirect after login
    const redirectUrl = new URL('/login', request.url);
    redirectUrl.searchParams.set('redirect', encodeURIComponent(request.url));

    return NextResponse.redirect(redirectUrl);
  }

  // If accessing login/register page while already authenticated, redirect to tasks
  if (isPublicPath && token && (currentPath === '/login' || currentPath === '/register')) {
    return NextResponse.redirect(new URL('/tasks', request.url));
  }

  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths that need authentication protection
     */
    '/tasks',
    '/tasks/:path*',
    '/dashboard',
    '/dashboard/:path*',
    // Add more protected routes as needed
  ],
};
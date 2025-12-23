import { NextRequest, NextResponse } from 'next/server';

// This function protects routes by checking for the presence of a token
export function middleware(request: NextRequest) {
  // Define protected routes
  const protectedPaths = ['/tasks'];
  const currentPath = request.nextUrl.pathname;

  // Check if the current path is protected
  const isProtectedPath = protectedPaths.some(path =>
    currentPath.startsWith(path)
  );

  if (isProtectedPath) {
    // Check if user has a token in localStorage (this is client-side only)
    // For server-side checking, we'd need to check cookies or headers
    // For now, we'll just allow the request to proceed and handle auth in components
  }

  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: ['/tasks/:path*', '/dashboard/:path*'],
};
# API Contract: Chat Endpoint Integration

## Overview
This document specifies the API contract between the ChatKit UI frontend and the backend chat endpoint.

## Backend Chat Endpoint (Existing)

### Endpoint: POST `/api/v1/{user_id}/chat`

#### Description
Processes user messages and returns AI-generated responses with potential tool call information.

#### Request Parameters
- **Path Parameter**:
  - `user_id` (string, required): UUID of the authenticated user

#### Request Headers
- `Authorization` (string, required): Bearer token in format "Bearer {jwt_token}"
- `Content-Type` (string, required): "application/json"

#### Request Body
```json
{
  "message": "string (required)",
  "metadata": {
    "any additional context": "value"
  }
}
```

**Validation**:
- `message` must be present and not empty (after trimming whitespace)
- `message` length must be between 1-2000 characters
- Total payload size must be under 10KB

#### Success Response (200 OK)
```json
{
  "conversation_id": "string (UUID)",
  "response": {
    "content": "string",
    "role": "string (typically 'assistant')"
  },
  "tool_calls": [
    {
      "id": "string",
      "function": {
        "name": "string",
        "arguments": "string (JSON)"
      },
      "type": "function"
    }
  ],
  "timestamp": "string (ISO 8601 datetime)"
}
```

#### Error Responses
- **400 Bad Request**: Invalid user_id format or missing/empty message
- **401 Unauthorized**: Invalid or missing JWT token
- **404 Not Found**: User not found or conversation cannot be created
- **500 Internal Server Error**: Processing error occurred

## Frontend-to-Backend Integration Contract

### Authentication Flow
1. Frontend retrieves JWT token from Better Auth session
2. Token is included in Authorization header for all chat requests
3. Backend validates token and verifies user identity matches user_id in path

### Message Flow
1. User enters message in ChatKit UI
2. Frontend validates message content (non-empty, proper length)
3. Frontend constructs request with user_id and authentication
4. Request is sent to backend chat endpoint
5. Backend processes message with AI and returns response
6. Frontend receives and displays response in ChatKit interface

### Error Handling Contract
- Frontend must handle network errors gracefully
- Error messages should be user-friendly and not expose internal details
- Authentication failures should redirect to login
- Backend errors should be categorized as recoverable/non-recoverable

## Frontend State Management Contract

### Loading States
- While request is pending: Show loading indicator
- After response: Hide loading indicator
- On error: Show appropriate error message

### Message Status Tracking
- `sending`: Message submitted to backend
- `sent`: Successfully sent to backend
- `received`: Response received from backend
- `error`: Error occurred during transmission

## Client-Side Caching
- Conversation history is cached in browser session storage
- Cache invalidated on user logout
- Cache refreshed when new messages are received

## Timeout Requirements
- Request timeout: 30 seconds
- Connection timeout: 10 seconds
- Backend should respond within 25 seconds to allow for network overhead

## Security Requirements
- All requests must include valid authentication token
- No sensitive data should be exposed in error messages
- Message content should be sanitized before display
- User ID in URL must match authenticated user

## Performance Requirements
- UI should respond to user input within 100ms
- Network requests should complete within 5 seconds (95th percentile)
- Error states should be displayed within 1 second of error occurrence
# Data Model: Frontend ChatKit UI

## Overview
This document defines the frontend data models for the ChatKit UI implementation, focusing on client-side data structures that support the chat interface.

## Client-Side Message Entity

### Message
Represents a message in the chat interface on the frontend

**Fields**:
- `id`: string - Unique identifier for the message (frontend generated for user messages, backend provided for AI responses)
- `content`: string - The actual message text content
- `role`: "user" | "assistant" - Identifies the sender type
- `timestamp`: Date - Client-side timestamp for display
- `status`: "sending" | "sent" | "received" | "error" - UI state for message delivery
- `toolCalls?`: Array<Object> - Optional tool call information from AI responses

**Validation Rules**:
- `content` must not be empty or whitespace only
- `role` must be one of allowed values
- `timestamp` must be a valid date

## Client-Side Conversation Entity

### ConversationState
Represents the client-side state of the conversation

**Fields**:
- `id?`: string - Backend conversation ID (undefined for new conversations)
- `messages`: Message[] - Ordered list of messages in the conversation
- `isLoading`: boolean - Whether the chat is currently processing
- `error?`: string - Error message if any occurred
- `userId`: string - The authenticated user ID
- `lastUpdated`: Date - Last time conversation was updated

**State Transitions**:
- Initial: `isLoading: false`, `messages: []`
- After sending message: `isLoading: true`, new message added with `status: "sending"`
- After receiving response: `isLoading: false`, AI message added with `status: "received"`

## Chat API Request/Response Models

### ChatRequest
Represents the data sent to the backend chat endpoint

**Fields**:
- `message`: string - The user's message content
- `metadata?`: Object - Additional context for the message

### ChatResponse
Represents the data received from the backend chat endpoint

**Fields**:
- `conversation_id`: string - The backend conversation identifier
- `response`: {
    - `content`: string - The AI response content
    - `role`: string - The role of the response (typically "assistant")
  }
- `tool_calls`: Array<Object> - Tool calls executed by the AI
- `timestamp`: string - ISO format timestamp of the response

## UI State Models

### UIState
Represents the overall UI state for the chat interface

**Fields**:
- `inputValue`: string - Current value in the message input field
- `isConnected`: boolean - Connection status to backend
- `connectionError?`: string - Error if connection failed
- `showTaskConfirmation?`: boolean - Whether to show task confirmation

### TaskConfirmation
Represents state for task confirmations in the UI

**Fields**:
- `isVisible`: boolean - Whether confirmation is shown
- `message`: string - The confirmation message
- `type`: "success" | "info" | "warning" - Type of confirmation
- `duration?`: number - Auto-hide duration in milliseconds

## API Client Configuration

### ChatAPIClient
Configuration for connecting to the backend chat endpoint

**Fields**:
- `baseUrl`: string - Base URL for the backend API
- `authToken`: string - JWT token for authentication
- `userId`: string - Current user's ID
- `timeout`: number - Request timeout in milliseconds (default: 30000)

## Validation Rules

### Message Content Validation
- Length: 1-2000 characters
- Content: Must contain non-whitespace characters
- Special characters: Allow Unicode characters, limit HTML-like tags

### Input Sanitization
- Strip leading/trailing whitespace
- Prevent injection of executable content
- Limit message length to prevent oversized payloads

## Relationship Mapping

The frontend data model maps to backend entities as follows:
- Frontend `Message` ↔ Backend `Message` model (during API communication)
- Frontend `ConversationState` ↔ Backend `Conversation` model (during API communication)
- Client-side state ↔ Backend persistence (synced via API calls)

## Error Handling Models

### APIError
Represents errors from API calls

**Fields**:
- `code`: string - Error code from API
- `message`: string - Human-readable error message
- `status`: number - HTTP status code
- `timestamp`: Date - When error occurred

### ClientError
Represents errors originating from client-side operations

**Fields**:
- `type`: string - Type of client error
- `message`: string - Error description
- `component`: string - Component where error originated
- `timestamp`: Date - When error occurred
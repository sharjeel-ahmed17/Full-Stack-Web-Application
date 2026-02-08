# Quickstart: Frontend ChatKit UI Development

## Prerequisites
- Node.js 18+ installed
- Python 3.13+ with uv package manager
- Running backend service with chat endpoint
- Valid authentication token

## Environment Setup

### 1. Install ChatKit Dependency
```bash
cd frontend
npm install @openai/chatkit-react
```

### 2. Verify Backend Connection
Ensure the backend chat endpoint is accessible:
- Endpoint: `POST /api/v1/{user_id}/chat`
- Test with curl or API client to verify functionality
- Confirm authentication system is working

## Development Commands

### Start Frontend Development Server
```bash
cd frontend
npm run dev
```

### Verify Chat Functionality
- Navigate to http://localhost:3000/chat (after implementation)
- Ensure authenticated user session is active
- Test sending and receiving messages

## Key Integration Points

### 1. Chat API Client
Create API client in `frontend/lib/api/chat.ts`:
- Handle authentication token inclusion
- Transform request/response formats as needed
- Manage loading/error states

### 2. Chat Component Structure
Create components in `frontend/components/chat/`:
- `ChatKitWrapper.tsx`: Main ChatKit integration
- `TaskConfirmation.tsx`: Task action confirmations

### 3. Page Integration
Create page in `frontend/app/chat/page.tsx`:
- Fetch user authentication status
- Initialize ChatKit with API adapter
- Handle task confirmations and errors

## Testing Strategy

### Unit Tests
```bash
npm run test
```

Test individual components and API client functions.

### E2E Tests
```bash
npm run test:e2e
```

Test complete chat workflow including authentication.

## API Configuration

### Environment Variables
Ensure these are configured in frontend `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

### Authentication Headers
- Retrieve JWT token from Better Auth session
- Include in `Authorization: Bearer {token}` header
- Handle token refresh if needed

## Common Issues & Solutions

### Issue: Authentication Failure
- **Cause**: Missing or invalid JWT token
- **Solution**: Verify user is logged in and token is properly attached

### Issue: API Connection Errors
- **Cause**: Backend service not running or incorrect URL
- **Solution**: Check backend status and API URL configuration

### Issue: Message Formatting
- **Cause**: Request/response format mismatch
- **Solution**: Verify ChatKit adapter properly transforms data

## Development Workflow

1. **Local Testing**: Test components in isolation
2. **Integration Testing**: Verify backend connection
3. **User Flow Testing**: Complete chat conversations
4. **Responsive Testing**: Verify mobile/desktop compatibility
5. **Error Scenario Testing**: Handle various error conditions

## Component Hierarchy
```
ChatPage
├── ChatKitWrapper
│   ├── TaskConfirmation
│   └── LoadingIndicator
└── API Client
    └── Auth Handler
```

## Performance Monitoring
- Track message send/receive times
- Monitor UI responsiveness during loading states
- Measure error rates and user recovery paths
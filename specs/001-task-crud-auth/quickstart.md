# Quickstart: Task CRUD with Authentication

**Feature Branch**: `001-task-crud-auth`
**Date**: 2025-12-14

## Prerequisites

- Docker Desktop installed and running
- Node.js 18+ (for local frontend development)
- Python 3.13+ with UV package manager (for local backend development)
- Git

## Quick Start (Docker Compose)

### 1. Clone and Checkout Feature Branch

```bash
git clone <repository-url>
cd Full-Stack-Web-Application
git checkout 001-task-crud-auth
```

### 2. Create Environment File

Create a `.env` file in the project root:

```bash
# Database (Local Development)
DATABASE_URL=postgresql://postgres:postgres@db:5432/todoapp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=todoapp

# Database (Production - Neon)
# NEON_DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require

# Authentication (CRITICAL: Use same secret for frontend and backend)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Backend Configuration
BACKEND_CORS_ORIGINS=http://localhost:3000
API_V1_PREFIX=/api/v1

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. Start All Services

```bash
docker-compose up --build
```

This starts:
- **Frontend**: http://localhost:3000 (Next.js)
- **Backend**: http://localhost:8000 (FastAPI)
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Database**: localhost:5432 (PostgreSQL)

### 4. Verify Services

```bash
# Check frontend
curl http://localhost:3000

# Check backend health
curl http://localhost:8000/health

# Check API docs
open http://localhost:8000/docs
```

## Local Development (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment with UV
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure

```
Full-Stack-Web-Application/
├── frontend/                 # Next.js 16+ App Router
│   ├── app/                  # Pages and layouts
│   ├── components/           # React components
│   ├── lib/                  # Utilities (auth, API client)
│   └── package.json
├── backend/                  # FastAPI + SQLModel
│   ├── src/
│   │   ├── api/              # Route handlers
│   │   ├── models/           # SQLModel models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic
│   ├── migrations/           # Alembic migrations
│   └── pyproject.toml
├── docker-compose.yml        # Container orchestration
├── .env                      # Environment variables (not committed)
└── specs/                    # Feature specifications
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login user | No |
| GET | `/api/v1/auth/me` | Get current user | Yes |
| GET | `/api/v1/tasks` | List user's tasks | Yes |
| POST | `/api/v1/tasks` | Create task | Yes |
| GET | `/api/v1/tasks/{id}` | Get task | Yes |
| PUT | `/api/v1/tasks/{id}` | Update task | Yes |
| DELETE | `/api/v1/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/v1/tasks/{id}/complete` | Toggle completion | Yes |

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Frontend Tests

```bash
cd frontend
npm run test
```

### E2E Tests

```bash
cd frontend
npm run test:e2e
```

## Common Commands

```bash
# Rebuild containers after dependency changes
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Run database migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Reset database
docker-compose down -v
docker-compose up --build

# Stop all services
docker-compose down
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `BETTER_AUTH_SECRET` | JWT signing secret (32+ chars) | Yes |
| `BETTER_AUTH_URL` | Auth callback URL | Yes |
| `BACKEND_CORS_ORIGINS` | Allowed CORS origins | Yes |
| `NEXT_PUBLIC_API_URL` | Backend API URL for frontend | Yes |

## Troubleshooting

### Database Connection Refused

```bash
# Ensure database is running
docker-compose ps

# Check database logs
docker-compose logs db
```

### Authentication Errors

- Ensure `BETTER_AUTH_SECRET` is identical in frontend and backend
- Check that cookies are being set (browser dev tools > Application > Cookies)

### CORS Errors

- Verify `BACKEND_CORS_ORIGINS` includes frontend URL
- Check browser console for specific CORS error messages

### Hot Reload Not Working

```bash
# Restart specific service
docker-compose restart frontend
docker-compose restart backend
```

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Follow Red-Green-Refactor cycle for each task
3. Ensure all tests pass before PR

# Full-Stack Web Application: Task CRUD with Authentication

A full-stack todo application with user authentication enabling task CRUD operations. Users can register, login, and manage their personal tasks (create, read, update, delete, toggle completion).

## Features

- User registration and authentication
- Secure JWT-based authentication
- Task management (Create, Read, Update, Delete)
- Toggle task completion status
- User data isolation (users only see their own tasks)
- Responsive web interface

## Tech Stack

- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLModel, Pydantic v2, Alembic
- **Database**: PostgreSQL 16
- **Authentication**: Better Auth + JWT
- **Deployment**: Docker Compose

## Prerequisites

- Docker Desktop installed and running
- Node.js 18+ (for local frontend development)
- Python 3.13+ with UV package manager (for local backend development)
- Git

## Quick Start (Docker Compose)

1. **Clone and Checkout Feature Branch**
   ```bash
   git clone <repository-url>
   cd Full-Stack-Web-Application
   git checkout 001-task-crud-auth
   ```

2. **Create Environment File**
   ```bash
   cp .env.example .env
   # Edit .env to set appropriate values
   ```

3. **Start All Services**
   ```bash
   docker-compose up --build
   ```

This starts:
- **Frontend**: http://localhost:3000 (Next.js)
- **Backend**: http://localhost:8000 (FastAPI)
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Database**: localhost:5432 (PostgreSQL)

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
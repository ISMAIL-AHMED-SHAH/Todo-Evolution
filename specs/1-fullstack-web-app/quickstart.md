# Quickstart Guide: Full-Stack Todo Web Application

**Date**: 2025-12-08
**Feature**: 1-fullstack-web-app
**Status**: Draft

## Overview

This guide provides instructions for setting up and running the Full-Stack Multi-User Todo Web Application locally. The application consists of a Next.js frontend and a FastAPI backend, with Neon Serverless PostgreSQL as the database.

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- Docker and Docker Compose
- pnpm or npm (pnpm recommended for better performance)

## Local Development Setup

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies

#### Frontend Dependencies
```bash
cd frontend
pnpm install  # or npm install
```

#### Backend Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the example environment file and update with your configuration:

```bash
# In the project root
cp .env.example .env
```

Required environment variables:
- `NEXT_PUBLIC_API_URL` - URL of the backend API
- `BETTER_AUTH_SECRET` - Secret for JWT token signing
- `DATABASE_URL` - Connection string for Neon PostgreSQL database
- `BETTER_AUTH_URL` - Base URL for Better Auth

### 4. Database Setup

1. Create a Neon Serverless PostgreSQL database
2. Set the `DATABASE_URL` in your `.env` file
3. Run database migrations:
```bash
cd backend
python -m alembic upgrade head
```

### 5. Running the Application

#### Option A: Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

#### Option B: Running Separately

##### Start Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000
```

##### Start Frontend
```bash
cd frontend
pnpm dev  # or npm run dev
```

The frontend will be available at http://localhost:3000

## API Endpoints

The application provides the following REST API endpoints:

### Task Management
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update task completion status

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/signin` - User login
- `GET /auth/profile` - Get user profile

## Authentication

The application uses Better Auth with JWT tokens for authentication:

1. Users register/sign in via the authentication endpoints
2. JWT tokens are returned upon successful authentication
3. Tokens must be included in the `Authorization: Bearer <token>` header for protected endpoints
4. The frontend automatically handles token storage and inclusion in requests

## Database Models

### User Model
- `id`: Primary key
- `email`: Unique, required
- `password_hash`: Securely hashed password
- `created_at`, `updated_at`: Timestamps

### Task Model
- `id`: Primary key
- `user_id`: Foreign key to User
- `title`: Required task title
- `description`: Optional task description
- `completed`: Boolean completion status
- `created_at`, `updated_at`: Timestamps

## Development Workflow

### Backend Development
1. Make changes to Python files in `backend/src/`
2. The server will automatically reload with `--reload` flag
3. Run tests with `pytest`:
```bash
cd backend
pytest
```

### Frontend Development
1. Make changes to React components in `frontend/src/`
2. The development server will automatically reload
3. Run tests with:
```bash
cd frontend
pnpm test  # or npm test
```

## Testing

### Backend Tests
```bash
cd backend
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

### Frontend Tests
```bash
cd frontend
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test -- --watch
```

## Deployment

### Environment Variables for Production
- `DATABASE_URL` - Production database connection string
- `BETTER_AUTH_SECRET` - Production JWT secret
- `BETTER_AUTH_URL` - Production base URL
- `NEXT_PUBLIC_API_URL` - Production API URL

### Docker Compose Deployment
```bash
# Build and deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify `DATABASE_URL` is correctly set
   - Ensure Neon PostgreSQL database is accessible
   - Check that migrations have been run

2. **Authentication Issues**
   - Verify `BETTER_AUTH_SECRET` matches between frontend and backend
   - Ensure JWT tokens are properly stored and sent with requests

3. **Frontend/Backend Communication**
   - Verify `NEXT_PUBLIC_API_URL` is correctly set
   - Check CORS settings in the backend

### Useful Commands

```bash
# Check backend API status
curl http://localhost:8000/health

# Run backend linter
cd backend
flake8 src/
black --check src/

# Run frontend linter
cd frontend
pnpm lint  # or npm run lint
```

## Next Steps

1. Implement the complete UI following the design specifications
2. Add additional user management features
3. Implement task categorization or tagging
4. Add task due dates and reminders
5. Implement data export functionality
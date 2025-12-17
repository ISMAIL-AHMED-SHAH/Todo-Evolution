# Claude Code Context for Full-Stack Todo Application

## Project Overview
- **Application**: Full-Stack Multi-User Todo Web Application
- **Architecture**: Next.js 16+ frontend with TypeScript and Tailwind CSS, Python FastAPI backend
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth with JWT tokens
- **Infrastructure**: Docker-Compose monorepo structure

## Technology Stack
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: Python 3.10+, FastAPI
- **Database**: Neon Serverless PostgreSQL, SQLModel ORM
- **Authentication**: Better Auth
- **Testing**: Jest (frontend), pytest (backend)
- **Containerization**: Docker, Docker Compose

## Key Architecture Patterns
- **Monorepo Structure**: Separate frontend/ and backend/ directories
- **RESTful API**: Following specific endpoint patterns:
  - GET/POST /api/{user_id}/tasks
  - GET/PUT/DELETE /api/{user_id}/tasks/{id}
  - PATCH /api/{user_id}/tasks/{id}/complete
- **JWT Authentication**: Tokens required on all API endpoints
- **User Isolation**: All operations enforce user ownership
- **Responsive Design**: Mobile-first approach with Tailwind CSS

## Next.js Configuration and Usage
- Use App Router for modern Next.js development
- Server components can fetch data with `fetch()` using cache options:
  - `{ cache: 'force-cache' }` for static data (like `getStaticProps`)
  - `{ cache: 'no-store' }` for dynamic data (like `getServerSideProps`)
  - `{ next: { revalidate: N } }` for ISR with N-second revalidation
- Use `layout.tsx` for root layout with `<html>` and `<body>` tags
- Client components use `'use client'` directive
- Use `useSearchParams` from `next/navigation` in App Router for URL parameters
- `<Link>` component for navigation with optional prefetching

## FastAPI and Authentication Patterns
- Use `OAuth2PasswordBearer` for JWT token authentication
- Implement dependency injection for current user validation
- Install `pyjwt` for JWT handling and `pwdlib` for password hashing
- Create authentication dependencies that validate tokens and return user data
- Use Pydantic models for request/response validation
- Implement nested dependencies pattern for user authentication:
  - `get_current_user` depends on token validation
  - `get_current_active_user` depends on `get_current_user` and checks active status
- Return proper HTTP status codes: 401 for unauthenticated, 403 for forbidden

## SQLModel Database Patterns
- Define base models with common fields, then inherit for different use cases:
  - `HeroBase` for common fields
  - `Hero` (table=True) for database table model
  - `HeroCreate` for creation payloads
  - `HeroPublic` for API responses
- Use `Relationship()` for relationships with `back_populates`
- Use `Field()` for column specifications including `index=True`, `foreign_key`, etc.
- Define separate models for API responses that include or exclude related data
- Use `Optional[int] = Field(default=None, primary_key=True)` for auto-incrementing IDs

## Better Auth Configuration
- Initialize with `betterAuth()` function and database configuration
- Use JWT plugin for JWT token generation and validation
- JWT tokens can be retrieved via `/api/auth/token` endpoint or client methods
- Use `createAuthClient()` with JWT plugin for client-side JWT operations
- Validate JWT tokens using `jose` library with remote JWKS:
  - `createRemoteJWKSet` for remote key validation
  - Verify issuer and audience match your BASE_URL
  - Handle token validation errors appropriately

## Neon PostgreSQL Connection Management
- Use `@neondatabase/serverless` package for serverless PostgreSQL connections
- In serverless environments (Vercel), create Pool/Client inside request handler
- Use `ctx.waitUntil(pool.end())` to properly close connections without blocking response
- Configure WebSocket constructor for Node.js v21 and earlier: `neonConfig.webSocketConstructor = ws`
- For direct queries, use the `neon()` function: `const sql = neon(process.env.DATABASE_URL)`
- Use `neonConfig.poolQueryViaFetch = true` for lower latency in experimental mode

## Tailwind CSS Configuration
- Configure via `tailwind.config.js` with `module.exports`
- Use `theme.extend` to add custom configurations
- Enable plugins via the `plugins` array: `plugins: [require("@tailwindcss/forms")]`
- Use `@config` directive in CSS files to specify different config files
- Configure responsive breakpoints in `theme.screens`
- For JIT (Just-in-Time) mode, use `mode: "jit"` in config
- Use container queries plugin for responsive designs based on container size

## Critical Requirements
- Multi-user data isolation (users can only access their own tasks)
- JWT token validation on all protected endpoints
- SQLModel ORM for all database operations
- Proper error handling with appropriate HTTP status codes
- Mobile-responsive UI design

## File Structure
```
project-root/
├── backend/
│   ├── src/
│   │   ├── models/      # SQLModel entities
│   │   ├── services/    # Business logic
│   │   ├── api/         # API routes
│   │   └── auth/        # Authentication logic
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   └── services/    # API service functions
│   └── tests/
├── specs/              # Specifications directory
├── docker-compose.yml
└── .env.example
```

## API Contract Summary
- All endpoints require `Authorization: Bearer <token>` header
- User ID in URL path must match authenticated user
- Proper HTTP status codes: 200, 201, 400, 401, 403, 404
- JSON request/response bodies with proper validation

## Database Schema
- **users table**: id, email (unique), password_hash, timestamps
- **tasks table**: id, user_id (FK), title, description, completed, timestamps
- Proper indexing on user_id for efficient queries
- Foreign key constraint between user_id and users.id

## Security Considerations
- JWT token validation middleware
- User ID verification in all data access operations
- Input validation using Pydantic models
- SQL injection prevention through ORM
- Proper session management

## Performance Guidelines
- API responses should complete within 2 seconds
- Use pagination for large result sets
- Proper database indexing
- Efficient component rendering in frontend

## Testing Strategy
- Unit tests for individual functions/services
- Integration tests for API endpoints
- Component tests for UI elements
- Multi-user scenario testing for data isolation

## Environment Variables
- `DATABASE_URL` - Database connection string
- `BETTER_AUTH_SECRET` - JWT signing secret
- `NEXT_PUBLIC_API_URL` - Backend API URL for frontend
- `BETTER_AUTH_URL` - Base URL for Better Auth

## Development Workflow
- Follow spec-driven development: specs → plan → tasks → implementation
- All changes must align with constitution principles
- Create PHRs for all significant changes
- Use feature branches with numbered prefixes (e.g., 1-fullstack-web-app)
# Quickstart Guide: Todo App UI/UX - Phase 2

**Last Updated**: 2025-12-15
**Feature**: 002-ui-ux-spec
**Estimated Setup Time**: 30-45 minutes

## Prerequisites

Before starting, ensure you have the following installed:

- **Node.js**: v18.0.0 or higher ([download](https://nodejs.org/))
- **Python**: 3.10 or higher ([download](https://www.python.org/downloads/))
- **PostgreSQL**: 15 or higher, OR **Neon account** ([neon.tech](https://neon.tech))
- **Git**: Latest version
- **Docker** (optional): For containerized development

**Verify installations**:
```bash
node --version  # Should show v18+
python --version  # Should show Python 3.10+
psql --version  # Should show PostgreSQL 15+ (if using local DB)
```

## Quick Setup (5 Minutes)

### 1. Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd transforming-todo

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

#### Frontend (.env.local)

Create `frontend/.env.local`:
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars

# Optional: Analytics, etc.
```

#### Backend (.env)

Create `backend/.env`:
```bash
# Database Configuration (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host/database

# Better Auth Shared Secret (MUST match frontend)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars

# Environment
ENVIRONMENT=development

# CORS Origins
ALLOWED_ORIGINS=http://localhost:3000

# Optional: Logging level
LOG_LEVEL=INFO
```

**Important**: The `BETTER_AUTH_SECRET` **must be identical** in both frontend and backend `.env` files for JWT verification to work.

### 3. Database Setup

#### Option A: Neon PostgreSQL (Recommended)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Paste into `backend/.env` as `DATABASE_URL`

#### Option B: Local PostgreSQL

```bash
# Create database
createdb todoapp_dev

# Update DATABASE_URL in backend/.env
DATABASE_URL=postgresql://localhost/todoapp_dev
```

#### Run Migrations

```bash
cd backend
source venv/bin/activate  # If not already activated

# Run Alembic migrations
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"
# Should show: users, tasks tables
```

### 4. Start Development Servers

#### Terminal 1: Backend (FastAPI)

```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Server running at http://localhost:8000
# API docs at http://localhost:8000/docs
```

#### Terminal 2: Frontend (Next.js)

```bash
cd frontend
npm run dev

# Server running at http://localhost:3000
```

### 5. Verify Setup

1. Open browser to `http://localhost:3000`
2. You should see the landing page or login page
3. Try creating an account
4. Navigate to dashboard and test task creation

---

## Development Workflow

### Working with Tasks

**Create a task**:
```bash
# Via UI: Click "Add Task" card on dashboard

# Via API (curl example):
curl -X POST http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task",
    "description": "Testing Phase 2 features",
    "priority": "High",
    "category": ["work", "urgent"],
    "due_date": "2025-12-20"
  }'
```

**List tasks**:
```bash
curl http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <your_jwt_token>"
```

**Filter overdue tasks**:
```bash
curl "http://localhost:8000/api/123/tasks?overdue=true" \
  -H "Authorization: Bearer <your_jwt_token>"
```

### ShadCN UI Components

**Add a new ShadCN component**:
```bash
cd frontend

# Example: Add a new button variant
npx shadcn@latest add button

# Example: Add dialog component
npx shadcn@latest add dialog
```

Components are copied to `frontend/src/components/ui/` where you can customize them.

### Framer Motion Animations

**Example: Add page transition**:
```tsx
// app/(dashboard)/dashboard/page.tsx
'use client';
import { motion } from 'framer-motion';
import { pageVariants } from '@/lib/animations';

export default function DashboardPage() {
  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageVariants}
    >
      {/* Page content */}
    </motion.div>
  );
}
```

### Database Migrations

**Create a new migration**:
```bash
cd backend
alembic revision --autogenerate -m "Add new field to tasks"

# Edit generated migration in alembic/versions/
# Apply migration
alembic upgrade head
```

**Rollback migration**:
```bash
alembic downgrade -1  # Go back one migration
```

---

## Testing

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/api/test_tasks.py
```

### E2E Tests (Playwright)

```bash
cd frontend

# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npm run test:e2e

# Run in UI mode
npm run test:e2e:ui
```

---

## Troubleshooting

### Issue: JWT Token Invalid (401 Unauthorized)

**Symptom**: All API requests return 401 even after login

**Solution**:
1. Check that `BETTER_AUTH_SECRET` is **identical** in frontend and backend `.env` files
2. Ensure secret is at least 32 characters
3. Restart both servers after changing `.env` files

### Issue: CORS Error in Browser Console

**Symptom**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
1. Verify `ALLOWED_ORIGINS=http://localhost:3000` in `backend/.env`
2. Check FastAPI CORS middleware configuration in `backend/src/main.py`
3. Ensure no trailing slash in origin URL

### Issue: Database Connection Error

**Symptom**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**:
1. Verify `DATABASE_URL` format: `postgresql://user:password@host:port/database`
2. For Neon: Check connection string includes `?sslmode=require`
3. Test connection: `psql $DATABASE_URL`

### Issue: ShadCN Components Not Styling Correctly

**Symptom**: Components appear unstyled or broken

**Solution**:
1. Ensure Tailwind CSS is configured: `npm run dev` should rebuild styles
2. Check `tailwind.config.ts` includes `./components/**/*.{ts,tsx}`
3. Verify `globals.css` imports: `@tailwind base; @tailwind components; @tailwind utilities;`

### Issue: Framer Motion Animations Not Working

**Symptom**: No animations, or console errors about motion

**Solution**:
1. Ensure component is a Client Component: Add `'use client';` at top
2. Check Framer Motion installed: `npm install framer-motion`
3. Verify variants are properly defined in `lib/animations.ts`

### Issue: Better Auth Session Not Persisting

**Symptom**: User gets logged out on page refresh

**Solution**:
1. Check cookies are enabled in browser
2. Verify `BETTER_AUTH_URL` matches your frontend URL
3. Check browser console for cookie errors
4. Ensure httpOnly cookies are allowed (same-origin)

---

## API Documentation

### Interactive API Docs

FastAPI provides auto-generated interactive documentation:

**Swagger UI**: http://localhost:8000/docs
- Test endpoints directly in browser
- View request/response schemas
- See all available endpoints

**ReDoc**: http://localhost:8000/redoc
- Alternative documentation view
- Better for reading API specs

### Example API Usage

**Get Session** (after login):
```typescript
// Frontend code
import { authClient } from '@/lib/auth-client';

const session = await authClient.getSession();
console.log(session);  // Session data with user info
```

**Make Authenticated API Call**:
```typescript
import { fetchAPI } from '@/lib/api-client';

// Automatic JWT injection
const tasks = await fetchAPI(`/api/${userId}/tasks`);
```

---

## Common Development Tasks

### Adding a New Page

1. Create page file in `frontend/src/app/`:
   ```tsx
   // src/app/(dashboard)/new-page/page.tsx
   export default function NewPage() {
     return <div>New Page</div>;
   }
   ```

2. Add to navigation (if needed):
   ```tsx
   // src/components/layout/Navbar.tsx
   <Link href="/new-page">New Page</Link>
   ```

### Adding a New API Endpoint

1. Create endpoint in `backend/src/api/`:
   ```python
   # src/api/tasks.py
   @router.get("/api/{user_id}/custom-endpoint")
   async def custom_endpoint(user_id: int):
       return {"message": "Hello"}
   ```

2. Add to frontend API client:
   ```typescript
   // src/lib/api-client.ts
   export const api = {
     tasks: {
       custom: (userId: string) =>
         fetchAPI(`/api/${userId}/custom-endpoint`),
     }
   };
   ```

### Customizing ShadCN Theme

Edit `frontend/tailwind.config.ts`:
```typescript
module.exports = {
  theme: {
    extend: {
      colors: {
        // Custom dashboard card colors
        'card-mint': '#a7f3d0',
        'card-purple': '#c4b5fd',
        // ...
      },
    },
  },
};
```

---

## Production Deployment

### Frontend (Vercel)

```bash
# Build for production
cd frontend
npm run build

# Deploy to Vercel
npx vercel --prod
```

**Environment Variables** (set in Vercel dashboard):
- `NEXT_PUBLIC_API_URL`: Your backend URL
- `BETTER_AUTH_SECRET`: Same as backend
- `BETTER_AUTH_URL`: Your frontend URL

### Backend (Railway/Render)

```bash
# Dockerfile already provided in backend/
# Push to GitHub and connect to Railway/Render

# Set environment variables in platform:
# - DATABASE_URL
# - BETTER_AUTH_SECRET
# - ALLOWED_ORIGINS
```

---

## Useful Commands Cheat Sheet

```bash
# Frontend
npm run dev          # Start dev server
npm run build        # Production build
npm run lint         # Run ESLint
npm test             # Run tests
npx shadcn@latest add <component>  # Add ShadCN component

# Backend
uvicorn src.main:app --reload  # Start dev server
alembic upgrade head            # Run migrations
alembic revision -m "msg"       # Create migration
pytest                          # Run tests
python -m pytest --cov=src      # Run with coverage

# Database
psql $DATABASE_URL              # Open PostgreSQL CLI
psql $DATABASE_URL -c "\dt"     # List tables
alembic current                 # Show current migration
alembic history                 # Show migration history

# Docker (optional)
docker-compose up               # Start all services
docker-compose down             # Stop all services
docker-compose logs -f frontend # View frontend logs
```

---

## Next Steps

1. **Read the Architecture Plan**: [specs/002-ui-ux-spec/plan.md](./plan.md)
2. **Review API Contracts**: [specs/002-ui-ux-spec/api-contracts.md](./api-contracts.md)
3. **Check Data Model**: [specs/002-ui-ux-spec/data-model.md](./data-model.md)
4. **Run `/sp.tasks`**: Break down implementation into tasks
5. **Start with Phase 0**: Set up ShadCN UI and Framer Motion

## Getting Help

- **API Documentation**: http://localhost:8000/docs
- **Project Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Spec-Kit-Plus Docs**: `.specify/` directory
- **Constitutional Principles**: `.specify/memory/constitution.md`

---

**Happy Coding!** 🚀

For detailed implementation guidance, refer to the [Implementation Plan](./plan.md).

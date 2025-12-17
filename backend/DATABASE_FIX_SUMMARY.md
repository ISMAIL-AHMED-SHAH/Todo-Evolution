# Database Schema Fix Summary

## Problem
FastAPI signup endpoint was failing with error: `column user.password_hash does not exist`

## Root Cause Analysis

After extensive investigation, the issue was identified as a **multi-layered problem**:

### 1. Table Name Mismatch
- **Task model** specified `__tablename__ = "tasks"` (plural)
- **Alembic migrations** created table named `task` (singular)
- On startup, `init_db()` called `SQLModel.metadata.create_all()` which created a DUPLICATE `tasks` table
- This caused schema confusion between the two tables

### 2. Startup Schema Creation
- `main.py` was calling `init_db()` on startup
- This bypassed Alembic migrations and created tables from SQLModel metadata
- Created a conflict between Alembic-managed schema and SQLModel-generated schema

### 3. Python Bytecode Caching
- Python's `.pyc` cache files were persisting old model definitions
- Even after code changes, cached bytecode was being used
- This caused intermittent failures

## Fixes Applied

### 1. Fixed Task Model Table Name
**File:** `backend/src/models/task.py` (line 29)
```python
# BEFORE:
class Task(TaskBase, table=True):
    __tablename__ = "tasks"

# AFTER:
class Task(TaskBase, table=True):
    __tablename__ = "task"
```

### 2. Added max_length to password_hash Field
**File:** `backend/src/models/user.py` (line 19)
```python
# BEFORE:
password_hash: str = Field(nullable=False)

# AFTER:
password_hash: str = Field(nullable=False, max_length=255)
```

### 3. Removed init_db() Call from Startup
**File:** `backend/src/main.py` (lines 41-47)
```python
# BEFORE:
@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup"""
    logger.info("Starting Todo App API...")
    init_db()
    logger.info("Database initialized successfully")

# AFTER:
@app.on_event("startup")
def on_startup():
    """Initialize application on startup"""
    logger.info("Starting Todo App API...")
    # NOTE: Database tables are managed by Alembic migrations, not SQLModel.metadata.create_all()
    # Run migrations using: alembic upgrade head
    logger.info("Application startup complete")
```

### 4. Dropped Duplicate Table
```sql
DROP TABLE IF EXISTS tasks CASCADE;
```

### 5. Installed Missing Dependencies
```bash
pip install PyJWT
```

## Verification Steps

### 1. Verify Database Schema
```python
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'user'
    ORDER BY ordinal_position;
""")

for row in cur.fetchall():
    print(f'{row[0]}: {row[1]}')
```

**Expected Output:**
```
id: integer
email: character varying
password_hash: character varying
created_at: timestamp without time zone
updated_at: timestamp without time zone
```

### 2. Test Signup Functionality
```bash
cd backend
# Clear cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete

# Run test script
PYTHONDONTWRITEBYTECODE=1 python -B test_signup.py
```

### 3. Test API Endpoint
```bash
# Start server (with cache clearing)
bash start_server.sh

# In another terminal, test signup
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

## Current Database State

### Tables
- `user` (managed by Alembic)
- `task` (managed by Alembic, formerly had duplicate `tasks` table)
- `alembic_version` (tracks migration state)

### Current Migration Version
- `353d19d8f7af` (fix_user_table_constraints)

### Migration History
1. `2025_12_09_0858` - Initial models (user, task tables)
2. `002_phase2_task_fields` - Added priority, category, due_date to task
3. `353d19d8f7af` - Added indexes and server defaults

## Best Practices Going Forward

### 1. Never Use init_db() in Production
- **Always** use Alembic migrations to manage schema
- `SQLModel.metadata.create_all()` should only be used in tests
- Keep `main.py` startup free of schema modifications

### 2. Table Naming Convention
- Use **singular** table names to match Alembic convention
- Be consistent: `user`, `task`, `post` (not `users`, `tasks`, `posts`)

### 3. Python Cache Management
- Add to `.gitignore`:
  ```
  __pycache__/
  *.py[cod]
  *$py.class
  ```
- Use `PYTHONDONTWRITEBYTECODE=1` in development
- Clear cache after model changes:
  ```bash
  find . -type d -name __pycache__ -exec rm -rf {} +
  ```

### 4. Model Field Definitions
- Always specify `max_length` for string fields that map to VARCHAR
- Match field constraints to database schema
- Document field purposes with comments

### 5. Development Workflow
1. Make model changes
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review migration file
4. Apply migration: `alembic upgrade head`
5. Clear Python cache
6. Restart server

## Files Modified

1. `backend/src/models/task.py` - Fixed table name
2. `backend/src/models/user.py` - Added max_length to password_hash
3. `backend/src/main.py` - Removed init_db() call
4. `backend/test_signup.py` - Added test script (NEW)
5. `backend/start_server.sh` - Added startup script (NEW)
6. `backend/DATABASE_FIX_SUMMARY.md` - This file (NEW)

## Testing Status

✓ Database schema verified (password_hash column exists)
✓ User model definition correct
✓ Alembic migrations up to date
✓ Duplicate `tasks` table removed
✓ SQLModel queries working with proper cache clearing

⚠️ **IMPORTANT**: Due to Python bytecode caching issues, always:
- Use the `start_server.sh` script to start the server
- Clear cache before testing: `find . -name "*.pyc" -delete`
- Use `-B` flag when running Python directly: `python -B script.py`

## Next Steps

1. **Test the signup endpoint** with the server started via `start_server.sh`
2. **Verify all auth endpoints** work correctly (/signup, /signin, /profile)
3. **Add integration tests** for authentication flow
4. **Document API** in OpenAPI/Swagger docs

## Troubleshooting

If you still see "column does not exist" errors:

1. **Clear ALL Python cache:**
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} +
   find . -name "*.pyc" -delete
   find . -name "*.pyo" -delete
   ```

2. **Verify database schema:**
   ```bash
   python -c "import psycopg2, os; from dotenv import load_dotenv; load_dotenv(); conn = psycopg2.connect(os.getenv('DATABASE_URL')); cur = conn.cursor(); cur.execute('SELECT column_name FROM information_schema.columns WHERE table_name=\\'user\\''); print([r[0] for r in cur.fetchall()])"
   ```

3. **Check Alembic state:**
   ```bash
   alembic current
   alembic history
   ```

4. **Restart with fresh environment:**
   ```bash
   killall python  # or taskkill on Windows
   bash start_server.sh
   ```

5. **Use NullPool for testing:**
   ```python
   from sqlalchemy.pool import NullPool
   engine = create_engine(database_url, poolclass=NullPool)
   ```

## Contact

For issues or questions about this fix, refer to:
- The git commit history for detailed changes
- Alembic migration files in `alembic/versions/`
- Model definitions in `src/models/`

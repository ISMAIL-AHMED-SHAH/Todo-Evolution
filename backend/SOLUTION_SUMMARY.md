# Database Connection Issue - Solution Summary

## Problem

FastAPI signup endpoint failed with error:
```
column user.password_hash does not exist
```

However:
- Direct psycopg2 queries worked
- Standalone SQLAlchemy tests worked
- Database schema verified to have password_hash column

## Root Causes Identified

### 1. Multiple .env Files with Different Databases (PRIMARY ISSUE)

**Problem**: Project had two `.env` files pointing to different Neon databases:

- **Root `.env`**: `npg_TSQ8nfG4PtZC@ep-mute-moon-a4ueuef7` (OLD database without password_hash)
- **backend/.env`**: `npg_5LyfV9UQjgWP@ep-old-lake-ahgffap2` (NEW database with password_hash)

The `database.py` file was loading from the root `.env` (project root), which pointed to an outdated database that didn't have the password_hash column after migrations.

**Solution**:
- Updated `database.py` to load from `backend/.env` instead of root `.env`
- Synchronized root `.env` to use the same database URL for consistency

### 2. Python Bytecode Cache (SECONDARY ISSUE)

**Problem**: Cached `.pyc` files from multiple Python versions (3.11 and 3.13) contained stale SQLAlchemy metadata from before schema migrations.

**Solution**:
- Cleared all `__pycache__` directories and `.pyc` files
- Created `clear_cache.sh` and `clear_cache.bat` scripts for future use
- Bytecode cache should be cleared after every database migration

## Files Modified

### 1. `backend/src/database/database.py`

**Changed** (line 21-23):
```python
# OLD: Loading from project root (WRONG)
env_path = Path(__file__).parent.parent.parent.parent / ".env"

# NEW: Loading from backend directory (CORRECT)
env_path = Path(__file__).parent.parent.parent / ".env"
```

**Added**: Diagnostic logging to verify database URL and model registration:
```python
logger.info(f"Database URL: {DATABASE_URL[:50]}...")
logger.info(f"Registered models: {list(SQLModel.metadata.tables.keys())}")
logger.info(f"User table columns in metadata: {user_columns}")
```

### 2. `backend/src/models/user.py`

**Enhanced**: Explicit column name configuration to prevent SQLAlchemy confusion:
```python
password_hash: str = Field(
    nullable=False,
    max_length=255,
    sa_column_kwargs={"name": "password_hash"}  # Explicit column name
)
```

### 3. `backend/alembic/env.py`

**Added**: Non-pooled endpoint logic to match `database.py`:
```python
# Use non-pooled endpoint for migrations to avoid schema cache
if "neon.tech" in database_url and "-pooler" in database_url:
    database_url = database_url.replace("-pooler", "")
```

### 4. `.env` (Root)

**Updated**: Synchronized to use the correct database URL matching `backend/.env`

## New Files Created

### 1. `backend/clear_cache.sh` & `backend/clear_cache.bat`

Scripts to clear Python bytecode cache:
```bash
# Linux/Mac
bash clear_cache.sh

# Windows
clear_cache.bat
```

### 2. `backend/diagnose_schema.py`

Diagnostic tool that checks:
- SQLModel metadata (Python model definitions)
- Database inspector (actual database schema)
- Direct SQL queries
- SQLAlchemy reflected metadata
- Test queries with SQLModel

Usage:
```bash
python diagnose_schema.py
```

### 3. `backend/test_sqlalchemy_connection.py`

Tests SQLAlchemy connection at different levels:
- Direct psycopg2
- SQLAlchemy Core (no models)
- SQLModel with models

### 4. `backend/DATABASE_TROUBLESHOOTING.md`

Comprehensive troubleshooting guide covering:
- Common database connection issues
- Python bytecode caching
- Neon pooled vs non-pooled endpoints
- Migration best practices
- Diagnostic tools usage

## Verification Steps

### 1. Verify Database URL

```bash
python -c "
from src.database.database import engine
import logging
logging.basicConfig(level=logging.INFO)
# Check logs for correct database URL
"
```

Expected output should show: `npg_5LyfV9UQjgWP@ep-old-lake-ahgffap2`

### 2. Run Diagnostic Tool

```bash
python diagnose_schema.py
```

All 5 tests should pass and show password_hash column.

### 3. Test FastAPI Import

```bash
python -c "from src.main import app; print('SUCCESS')"
```

Should print "SUCCESS" with no errors.

### 4. Test Signup Endpoint

```bash
python test_fastapi_flow.py
```

Should successfully query User model.

## Prevention Tips

### 1. Always Clear Cache After Migrations

```bash
bash clear_cache.sh
alembic upgrade head
```

### 2. Use Single Source of Truth for DATABASE_URL

Keep `backend/.env` and root `.env` synchronized, or better yet, use only `backend/.env`.

### 3. Verify Database Connection After Changes

Run `python diagnose_schema.py` after:
- Database migrations
- Model changes
- Environment variable updates
- Switching between pooled/non-pooled endpoints

### 4. Development Workflow

```bash
# 1. Make model changes
vim src/models/user.py

# 2. Clear cache
bash clear_cache.sh

# 3. Generate migration
alembic revision --autogenerate -m "description"

# 4. Review migration
cat alembic/versions/YYYY_MM_DD_HHMM-*.py

# 5. Apply migration
alembic upgrade head

# 6. Verify
python diagnose_schema.py

# 7. Restart server
# Ctrl+C and restart uvicorn
```

### 5. Use Environment-Specific .env Files

Consider using:
- `backend/.env.local` - Your local development (gitignored)
- `backend/.env.example` - Template for team
- Root `.env` - Docker/global configuration only

## Key Takeaways

1. **Multiple .env files can cause database confusion** - Always verify which .env file is being loaded
2. **Python bytecode cache persists stale metadata** - Clear cache after schema changes
3. **Neon pooled vs non-pooled endpoints** - Use non-pooled for development to avoid cache
4. **Diagnostic tools are essential** - Created tools to quickly identify issues
5. **Explicit configuration prevents ambiguity** - Use explicit column names and logging

## Current Status

✅ FastAPI server imports successfully
✅ Database connection uses correct database
✅ SQLModel metadata includes password_hash column
✅ Direct queries work
✅ SQLAlchemy queries work
✅ All diagnostic tests pass

## Next Steps

1. Start FastAPI server: `uvicorn src.main:app --reload`
2. Test signup endpoint with Postman/curl
3. Verify authentication flow end-to-end
4. Consider migrating away from dual .env setup

## Contact for Issues

If you encounter similar issues:

1. Run `python diagnose_schema.py`
2. Check which .env file is being loaded
3. Verify DATABASE_URL in logs
4. Clear Python cache: `bash clear_cache.sh`
5. Check `DATABASE_TROUBLESHOOTING.md` for more details

---

## Additional Issue: Bcrypt Python 3.13 Compatibility

After resolving the database connection issue, a secondary error emerged during password hashing:

### Problem

```
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary
```

This error occurred in `backend/src/auth/auth_handler.py` when the signup endpoint attempted to hash passwords using passlib's CryptContext with bcrypt.

### Root Cause

The passlib library has compatibility issues with Python 3.13. During bcrypt backend initialization, passlib attempts to detect bcrypt's "wrap bug" by passing a test password, but this fails with the Python 3.13 runtime due to internal changes in how bcrypt handles password length validation.

### Solution

Replaced passlib's CryptContext with direct bcrypt usage in `backend/src/auth/auth_handler.py`:

**Before**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

**After**:
```python
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
```

### Verification

All authentication endpoints now work correctly:

1. **Signup Test**: ✅
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"bcrypt-test@example.com","password":"testpass123"}'

# Response: {"id":2,"email":"bcrypt-test@example.com"}
```

2. **Signin Test**: ✅
```bash
curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"bcrypt-test@example.com","password":"testpass123"}'

# Response: {"access_token":"eyJ...","token_type":"bearer"}
```

3. **Protected Endpoint Test**: ✅
```bash
curl -X GET http://localhost:8000/auth/profile \
  -H "Authorization: Bearer <token>"

# Response: {"id":2,"email":"bcrypt-test@example.com","created_at":"...","updated_at":"..."}
```

### Key Takeaways

1. **Python 3.13 compatibility**: Always test third-party authentication libraries with the target Python version
2. **Direct library usage**: Sometimes using libraries directly (bcrypt) is more reliable than abstraction layers (passlib)
3. **Progressive testing**: Database connection → Password hashing → Authentication flow

---

**Resolution Date**: 2025-12-17
**Issues Resolved**:
1. Database connection (.env files + bytecode cache)
2. Bcrypt Python 3.13 compatibility (passlib → direct bcrypt)
**Total Duration**: ~3 hours
**Status**: FULLY RESOLVED ✅

## Complete Authentication Flow Status

✅ Backend FastAPI server running on port 8000
✅ Frontend Next.js server running on port 3000
✅ Database connection verified (password_hash column accessible)
✅ User signup working (bcrypt password hashing)
✅ User signin working (JWT token generation)
✅ Protected endpoints working (JWT validation)
✅ Complete end-to-end authentication flow operational

# Database Connection Troubleshooting Guide

This document addresses common database connection issues with Neon PostgreSQL and SQLAlchemy/SQLModel.

## Issue: "Column does not exist" Error

### Symptoms
- FastAPI endpoint fails with error: `column user.password_hash does not exist`
- Direct database queries work fine
- Standalone SQLAlchemy scripts work fine
- Only FastAPI server has the issue

### Root Cause
**Python Bytecode Caching** - Python compiles .py files to .pyc bytecode files for faster loading. When schema changes occur (migrations, model updates), these cached files can contain stale metadata from the old schema.

This issue is particularly common when:
- Switching between Python versions (3.11 vs 3.13)
- After running database migrations
- After modifying SQLModel model definitions
- Using both pooled and non-pooled Neon endpoints

### Solution

#### Quick Fix: Clear Python Cache
```bash
# Linux/Mac
bash clear_cache.sh

# Windows
clear_cache.bat

# Manual (Linux/Mac)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Manual (Windows)
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
del /s /q *.pyc
```

#### Then restart your server:
```bash
# Stop the server (Ctrl+C)
# Then restart:
python src/main.py
# or
uvicorn src.main:app --reload
```

## Neon PostgreSQL Endpoint Selection

### Pooled vs Non-Pooled Endpoints

#### Pooled Endpoint (Connection Pooler)
- Format: `postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/db`
- Use for: Production, high-traffic applications
- Pros: Better connection management, faster cold starts
- Cons: May cache schema metadata

#### Non-Pooled Endpoint (Direct)
- Format: `postgresql://user:pass@ep-xxx.region.aws.neon.tech/db` (no `-pooler`)
- Use for: Development, after migrations
- Pros: Always fresh schema, no caching
- Cons: Slightly slower connection establishment

### Configuration

The application automatically uses the non-pooled endpoint in development:

```python
# In database.py
if "neon.tech" in DATABASE_URL and "-pooler" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("-pooler", "")
```

This ensures schema changes are immediately visible.

## Migration Best Practices

### After Creating a Migration

1. **Clear Python cache** (always!)
   ```bash
   bash clear_cache.sh  # or clear_cache.bat on Windows
   ```

2. **Apply the migration**
   ```bash
   alembic upgrade head
   ```

3. **Verify schema**
   ```bash
   python diagnose_schema.py
   ```

4. **Restart your server**
   Stop (Ctrl+C) and restart the FastAPI server

### Migration Workflow

```bash
# 1. Generate migration from model changes
alembic revision --autogenerate -m "description"

# 2. Review the generated migration file
cat alembic/versions/YYYY_MM_DD_HHMM-<hash>_description.py

# 3. Clear cache (IMPORTANT!)
bash clear_cache.sh

# 4. Apply migration
alembic upgrade head

# 5. Verify with diagnostic tool
python diagnose_schema.py

# 6. Restart server
# Stop and restart your uvicorn process
```

## Diagnostic Tools

### diagnose_schema.py

Run this script to compare SQLModel metadata, database schema, and test queries:

```bash
python diagnose_schema.py
```

This will show:
1. SQLModel metadata (Python model definitions)
2. Database inspector (actual database schema)
3. Direct SQL query results
4. SQLAlchemy reflected metadata
5. Test query with SQLModel

All five should match. If they don't, you have a cache or configuration issue.

### test_fastapi_flow.py

Simulates FastAPI's import and initialization flow:

```bash
python test_fastapi_flow.py
```

This helps identify if the issue is specific to FastAPI or a general problem.

## Common Issues and Solutions

### Issue: Multiple Python Versions

**Problem**: You have .pyc files from both Python 3.11 and 3.13

**Solution**:
```bash
# Clear all cache files
bash clear_cache.sh

# Use a specific Python version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Model Changes Not Reflected

**Problem**: You changed a model but queries still use old schema

**Solution**:
1. Clear cache: `bash clear_cache.sh`
2. Generate migration: `alembic revision --autogenerate -m "model changes"`
3. Apply migration: `alembic upgrade head`
4. Restart server

### Issue: Alembic and App Use Different Endpoints

**Problem**: Alembic uses pooled endpoint, app uses non-pooled (or vice versa)

**Solution**: Both now use the same logic (see `alembic/env.py` and `src/database/database.py`)

## Prevention Tips

1. **Always clear cache after migrations**
   ```bash
   bash clear_cache.sh && alembic upgrade head
   ```

2. **Use virtual environments**
   Prevents conflicts between Python versions

3. **Add to your workflow**
   ```bash
   # .git/hooks/post-merge (auto-clear after git pull)
   #!/bin/bash
   bash backend/clear_cache.sh
   ```

4. **Use `--reload` carefully**
   Uvicorn's `--reload` should handle cache, but manual clearing is safer

5. **Monitor schema changes**
   Run `python diagnose_schema.py` after any database changes

## SQLModel Configuration

### Model Definition Best Practices

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}  # Allow model redefinition

    # Explicit column names prevent confusion
    id: int = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(
        nullable=False,
        max_length=255,
        sa_column_kwargs={"name": "password_hash"}  # Explicit DB column name
    )
```

### Engine Configuration

```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,       # Check connection health
    pool_recycle=300,         # Recycle after 5 min
    echo=not IS_PRODUCTION,   # Log SQL in dev
)
```

## Need More Help?

1. Check Neon dashboard for connection stats
2. Review application logs for SQLAlchemy warnings
3. Run diagnostic script: `python diagnose_schema.py`
4. Check Alembic migration history: `alembic history`
5. Verify current schema version: `alembic current`

## Quick Reference

```bash
# Clear cache (do this often!)
bash clear_cache.sh

# Check schema
python diagnose_schema.py

# Migration workflow
alembic revision --autogenerate -m "changes"
bash clear_cache.sh
alembic upgrade head

# Check migration status
alembic current
alembic history

# Restart server
# Ctrl+C then:
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

```env
# Use pooled endpoint in production
DATABASE_URL=postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/db

# The app automatically switches to non-pooled in development
# No need to manually change the URL
```

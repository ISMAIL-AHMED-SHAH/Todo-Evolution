#!/usr/bin/env python
"""
Force schema refresh by clearing metadata and testing fresh
"""
import sys
sys.dont_write_bytecode = True

import os
from dotenv import load_dotenv
load_dotenv()

# Clear any cached modules
for key in list(sys.modules.keys()):
    if 'src' in key or 'models' in key:
        del sys.modules[key]

# Now import fresh
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy.pool import NullPool

# Import models - this registers them with SQLModel.metadata
from src.models.user import User
from src.models.task import Task

database_url = os.getenv('DATABASE_URL')

print("=== Force Schema Refresh Test ===\n")

# Clear metadata
print("Clearing SQLModel metadata...")
SQLModel.metadata.clear()

# Create fresh engine with no pooling
engine = create_engine(database_url, poolclass=NullPool)

# Reflect database schema
print("Reflecting database schema...")
SQLModel.metadata.reflect(bind=engine)

print(f"Tables in metadata: {list(SQLModel.metadata.tables.keys())}\n")

if 'user' in SQLModel.metadata.tables:
    user_table = SQLModel.metadata.tables['user']
    print("User table columns from reflection:")
    for col in user_table.columns:
        print(f"  - {col.name}: {col.type}")
    print()

# Now try query
print("Testing query...")
try:
    with Session(engine) as session:
        # Try simple select
        result = session.execute(select(user_table)).fetchall()
        print(f"SUCCESS: Raw table select worked! Found {len(result)} rows\n")
except Exception as e:
    print(f"FAILED: Raw table select failed: {e}\n")

# Now test with User model - reimport to get fresh class
from importlib import reload
import src.models.user as user_module
reload(user_module)
from src.models.user import User as FreshUser

print("Testing with fresh User model...")
try:
    with Session(engine) as session:
        users = session.exec(select(FreshUser)).all()
        print(f"SUCCESS! Found {len(users)} users")
        for u in users:
            print(f"  - {u.email} (has password_hash: {hasattr(u, 'password_hash')})")
except Exception as e:
    print(f"FAILED: {e}")

print("\nDone.")

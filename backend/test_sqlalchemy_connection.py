"""
Debug SQLAlchemy connection and query generation
"""
import os
import sys
sys.dont_write_bytecode = True

from dotenv import load_dotenv
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv('DATABASE_URL')
if '-pooler' in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('-pooler', '')
    print("[DEBUG] Using non-pooled endpoint")

print(f"DATABASE_URL: {DATABASE_URL[:60]}...")

# Test 1: Direct psycopg2
print("\n" + "=" * 80)
print("Test 1: Direct psycopg2 query")
print("=" * 80)

import psycopg2
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute('SELECT column_name FROM information_schema.columns WHERE table_name = %s', ('user',))
print(f"Columns in user table: {[row[0] for row in cur.fetchall()]}")
cur.close()
conn.close()

# Test 2: SQLAlchemy without models
print("\n" + "=" * 80)
print("Test 2: SQLAlchemy Core (no models)")
print("=" * 80)

from sqlalchemy import create_engine, text, inspect
engine = create_engine(DATABASE_URL, echo=True)

with engine.connect() as conn:
    result = conn.execute(text('SELECT * FROM "user" LIMIT 1'))
    row = result.first()
    if row:
        print(f"Found row with keys: {row._mapping.keys()}")
    else:
        print("No rows in table")

# Check inspector
inspector = inspect(engine)
cols = inspector.get_columns('user')
print(f"\nInspector columns: {[col['name'] for col in cols]}")

# Test 3: SQLModel with models
print("\n" + "=" * 80)
print("Test 3: SQLModel with models")
print("=" * 80)

from sqlmodel import SQLModel, Session, select

# Import models to register
from src.models.user import User

print(f"SQLModel metadata tables: {list(SQLModel.metadata.tables.keys())}")

if 'user' in SQLModel.metadata.tables:
    user_table = SQLModel.metadata.tables['user']
    cols = [col.name for col in user_table.columns]
    print(f"User table metadata columns: {cols}")

# Try query
try:
    with Session(engine) as session:
        stmt = select(User).limit(1)
        print(f"\nExecuting: {stmt}")
        result = session.exec(stmt).first()
        if result:
            print(f"SUCCESS! User: {result.email}")
        else:
            print("No users found")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("Tests complete")
print("=" * 80)

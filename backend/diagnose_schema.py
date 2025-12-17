"""
Diagnostic script to inspect SQLAlchemy metadata and database schema
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import inspect, text
from sqlmodel import SQLModel, create_engine, Session

# Import models to register with metadata
from src.models.user import User
from src.models.task import Task

print("=" * 80)
print("DIAGNOSTIC: SQLAlchemy Metadata vs Database Schema")
print("=" * 80)

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Apply same non-pooler logic as database.py
if "neon.tech" in DATABASE_URL and "-pooler" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("-pooler", "")
    print("[DIAGNOSTIC] Switched to non-pooled endpoint")

print(f"\nDatabase URL: {DATABASE_URL[:60]}...")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

print("\n" + "=" * 80)
print("1. SQLModel Metadata (Python Model Definitions)")
print("=" * 80)

if 'user' in SQLModel.metadata.tables:
    user_table = SQLModel.metadata.tables['user']
    print(f"\nUser table columns from SQLModel.metadata:")
    for col in user_table.columns:
        print(f"  - {col.name}: {col.type} (nullable={col.nullable})")
else:
    print("\nERROR: 'user' table not found in SQLModel.metadata!")

print("\n" + "=" * 80)
print("2. Database Inspector (Actual Database Schema)")
print("=" * 80)

inspector = inspect(engine)

# Get actual columns from database
actual_columns = inspector.get_columns('user')
print(f"\nUser table columns from database:")
for col in actual_columns:
    print(f"  - {col['name']}: {col['type']} (nullable={col['nullable']})")

print("\n" + "=" * 80)
print("3. Direct SQL Query")
print("=" * 80)

with Session(engine) as session:
    # Get column names via information_schema
    result = session.exec(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'user'
        ORDER BY ordinal_position
    """))

    print(f"\nUser table columns from information_schema:")
    for row in result:
        print(f"  - {row[0]}: {row[1]} (nullable={row[2]})")

print("\n" + "=" * 80)
print("4. SQLAlchemy Reflected Metadata")
print("=" * 80)

# Create a fresh metadata and reflect from database
from sqlalchemy import MetaData, Table
reflected_metadata = MetaData()
reflected_user = Table('user', reflected_metadata, autoload_with=engine)

print(f"\nUser table columns from reflection:")
for col in reflected_user.columns:
    print(f"  - {col.name}: {col.type} (nullable={col.nullable})")

print("\n" + "=" * 80)
print("5. Test Query with SQLModel")
print("=" * 80)

try:
    with Session(engine) as session:
        from sqlmodel import select
        statement = select(User).limit(1)
        print(f"\nGenerated SQL:")
        print(f"{statement}")

        result = session.exec(statement).first()
        if result:
            print(f"\nQuery SUCCESS - Found user: {result.email}")
            print(f"User has password_hash: {hasattr(result, 'password_hash')}")
        else:
            print(f"\nQuery SUCCESS - No users in database")
except Exception as e:
    print(f"\nQuery FAILED with error:")
    print(f"  {type(e).__name__}: {e}")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)

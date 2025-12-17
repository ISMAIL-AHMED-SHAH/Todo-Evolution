"""
Test script that simulates FastAPI's import flow
"""
import sys
from pathlib import Path

# Add src to path (same as main.py would do)
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("Simulating FastAPI Startup Flow")
print("=" * 80)

# Step 1: Load environment (as .env would be loaded)
print("\n1. Loading environment variables...")
from dotenv import load_dotenv
load_dotenv()

# Step 2: Import database module (this creates the engine)
print("\n2. Importing database module...")
from src.database import get_session

# Step 3: Import models via auth router
print("\n3. Importing auth router (which imports models)...")
from src.api.auth import router as auth_router

# Step 4: Try to use the session
print("\n4. Testing database session...")
from sqlmodel import select, Session
from src.models.user import User
from src.database.database import engine

with Session(engine) as session:
    try:
        print("\n5. Executing query...")
        statement = select(User).limit(1)
        print(f"   SQL: {statement}")

        result = session.exec(statement).first()

        if result:
            print(f"\n   SUCCESS! Found user: {result.email}")
            print(f"   User ID: {result.id}")
            print(f"   Has password_hash: {hasattr(result, 'password_hash')}")
            if hasattr(result, 'password_hash'):
                print(f"   password_hash length: {len(result.password_hash)}")
        else:
            print(f"\n   SUCCESS! No users found (empty table)")

    except Exception as e:
        print(f"\n   FAILED with error:")
        print(f"   {type(e).__name__}: {e}")

        # Print detailed error info
        import traceback
        print("\n   Traceback:")
        traceback.print_exc()

print("\n" + "=" * 80)
print("Test Complete")
print("=" * 80)

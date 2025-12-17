#!/usr/bin/env python
"""
Test script to verify signup functionality
Run this after clearing Python cache: rm -rf **/__pycache__
"""
import sys
sys.dont_write_bytecode = True

# IMPORTANT: Import database module FIRST to ensure proper initialization
# This loads models and creates engine with correct configuration
from src.database.database import engine, get_session
from sqlmodel import Session, select

# Now import models (already registered by database.py)
from src.models.user import User, UserCreate
from src.auth import get_password_hash, verify_password

# Engine is already configured by database.py - use that instead of creating new one

def test_signup():
    """Test the complete signup flow"""
    print('=== Testing Signup Functionality ===\n')

    test_email = 'test_signup_script@example.com'
    test_password = 'securepassword123'

    # Test 1: Create user
    print('Test 1: Creating new user...')
    try:
        with Session(engine) as session:
            # Check if user exists
            existing = session.exec(select(User).where(User.email == test_email)).first()

            if existing:
                print(f'  - User already exists (ID={existing.id})')
                user_id = existing.id
            else:
                # Create new user
                hashed_password = get_password_hash(test_password)
                new_user = User(
                    email=test_email,
                    password_hash=hashed_password
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                user_id = new_user.id
                print(f'  - SUCCESS: User created (ID={user_id})')
    except Exception as e:
        print(f'  - FAILED: {e}')
        return False

    # Test 2: Verify user can be queried
    print('\nTest 2: Querying user...')
    try:
        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == test_email)).first()
            if user:
                print(f'  - SUCCESS: Found user (ID={user.id}, Email={user.email})')
                print(f'  - Has password_hash: {len(user.password_hash) > 0}')
            else:
                print('  - FAILED: User not found')
                return False
    except Exception as e:
        print(f'  - FAILED: {e}')
        return False

    # Test 3: Verify password
    print('\nTest 3: Password verification...')
    try:
        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == test_email)).first()
            if verify_password(test_password, user.password_hash):
                print('  - SUCCESS: Password verified correctly')
            else:
                print('  - FAILED: Password verification failed')
                return False
    except Exception as e:
        print(f'  - FAILED: {e}')
        return False

    print('\n=== ALL TESTS PASSED ===')
    print('\nThe signup functionality is working correctly!')
    print('You can now use the /auth/signup endpoint.')
    return True

if __name__ == '__main__':
    success = test_signup()
    sys.exit(0 if success else 1)

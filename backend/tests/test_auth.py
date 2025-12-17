"""
Unit tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_signup_success():
    """Test successful user registration"""
    response = client.post(
        "/auth/signup",
        json={
            "email": "newuser@example.com",
            "password": "SecurePassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "newuser@example.com"
    assert "password" not in data  # Password should not be returned


def test_signup_duplicate_email():
    """Test signup with existing email"""
    # First signup
    client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "SecurePassword123"
        }
    )

    # Try to signup again with same email
    response = client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "AnotherPassword456"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_signin_success():
    """Test successful login"""
    # First create a user
    client.post(
        "/auth/signup",
        json={
            "email": "testlogin@example.com",
            "password": "SecurePassword123"
        }
    )

    # Now sign in
    response = client.post(
        "/auth/signin",
        json={
            "email": "testlogin@example.com",
            "password": "SecurePassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_signin_wrong_password():
    """Test login with incorrect password"""
    # Create a user
    client.post(
        "/auth/signup",
        json={
            "email": "wrongpass@example.com",
            "password": "CorrectPassword123"
        }
    )

    # Try to sign in with wrong password
    response = client.post(
        "/auth/signin",
        json={
            "email": "wrongpass@example.com",
            "password": "WrongPassword456"
        }
    )
    assert response.status_code == 400


def test_signin_nonexistent_user():
    """Test login with non-existent user"""
    response = client.post(
        "/auth/signin",
        json={
            "email": "nonexistent@example.com",
            "password": "SomePassword123"
        }
    )
    assert response.status_code == 400


def test_get_profile_authenticated():
    """Test getting profile with valid token"""
    # Create and login a user
    client.post(
        "/auth/signup",
        json={
            "email": "profile@example.com",
            "password": "SecurePassword123"
        }
    )

    login_response = client.post(
        "/auth/signin",
        json={
            "email": "profile@example.com",
            "password": "SecurePassword123"
        }
    )
    token = login_response.json()["access_token"]

    # Get profile
    response = client.get(
        "/auth/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "profile@example.com"


def test_get_profile_unauthenticated():
    """Test getting profile without token"""
    response = client.get("/auth/profile")
    assert response.status_code in [401, 403]  # Unauthorized

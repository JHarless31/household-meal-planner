"""
Tests for Authentication API
"""

import pytest
from fastapi import status


class TestAuthentication:
    """Test authentication endpoints"""

    def test_register_user(self, client):
        """Test user registration"""
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "password" not in data

    def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "different@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "testpassword123"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "user" in data
        assert data["user"]["username"] == "testuser"
        assert "session" in response.cookies

    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        response = client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, client, auth_headers):
        """Test get current user"""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"

    def test_logout(self, client, auth_headers):
        """Test logout"""
        response = client.post("/api/auth/logout", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK

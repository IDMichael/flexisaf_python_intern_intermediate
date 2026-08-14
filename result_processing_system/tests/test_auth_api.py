from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.security import (
    create_access_token,
    hash_password,
)
from app.database.connection import create_connection


client = TestClient(app)


# ---------------------------------------------------------
# Test database helpers
# ---------------------------------------------------------

def create_test_user(
    username="testuser",
    password="TestPassword123!",
    role="student",
    is_active=1,
):
    connection = create_connection()

    cursor = connection.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users (
            username,
            password_hash,
            role,
            is_active
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            password_hash,
            role,
            is_active,
        ),
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def delete_test_user(username):
    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        (username,),
    )

    connection.commit()
    connection.close()


# ---------------------------------------------------------
# User creation
# ---------------------------------------------------------

def test_user_can_be_created():

    username = "create_test_user"

    try:
        user_id = create_test_user(
            username=username,
        )

        assert user_id is not None

    finally:
        delete_test_user(username)


# ---------------------------------------------------------
# Password security
# ---------------------------------------------------------

def test_password_is_hashed():

    username = "hash_test_user"

    try:
        create_test_user(
            username=username,
            password="MyPassword123!",
        )

        connection = create_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT password_hash
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        row = cursor.fetchone()

        connection.close()

        assert row is not None

        password_hash = row[0]

        assert password_hash != (
            "MyPassword123!"
        )

        assert password_hash.startswith(
            "$2"
        )

    finally:
        delete_test_user(username)


# ---------------------------------------------------------
# Successful login
# ---------------------------------------------------------

def test_successful_login():

    username = "login_test_user"
    password = "LoginPassword123!"

    try:
        create_test_user(
            username=username,
            password=password,
            role="student",
        )

        response = client.post(
            "/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"

        assert data["access_token"]

    finally:
        delete_test_user(username)


# ---------------------------------------------------------
# Wrong password
# ---------------------------------------------------------

def test_wrong_password_is_rejected():

    username = "wrong_password_user"

    try:
        create_test_user(
            username=username,
            password="CorrectPassword123!",
        )

        response = client.post(
            "/auth/login",
            json={
                "username": username,
                "password": "WrongPassword123!",
            },
        )

        assert response.status_code == 401

    finally:
        delete_test_user(username)


# ---------------------------------------------------------
# Nonexistent user
# ---------------------------------------------------------

def test_nonexistent_user_is_rejected():

    delete_test_user(
        "user_that_does_not_exist"
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "user_that_does_not_exist",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401


# ---------------------------------------------------------
# Protected endpoint without authentication
# ---------------------------------------------------------

def test_protected_endpoint_requires_authentication():

    response = client.get(
        "/advanced-analytics/grades"
    )

    assert response.status_code == 401


# ---------------------------------------------------------
# Valid token
# ---------------------------------------------------------

def test_valid_token_allows_access():

    username = "valid_token_user"

    try:
        create_test_user(
            username=username,
            password="Password123!",
            role="student",
        )

        login_response = client.post(
            "/auth/login",
            json={
                "username": username,
                "password": "Password123!",
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()[
            "access_token"
        ]

        response = client.get(
            "/advanced-analytics/grades",
            headers={
                "Authorization":
                f"Bearer {token}"
            },
        )

        assert response.status_code != 401

    finally:
        delete_test_user(username)


# ---------------------------------------------------------
# Expired token
# ---------------------------------------------------------

def test_expired_token_is_rejected():

    token = create_access_token(
        {
            "sub": "1",
            "username": "expired_user",
            "role": "student",
        },
        expires_delta=timedelta(
            seconds=-1
        ),
    )

    response = client.get(
        "/advanced-analytics/grades",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
    )

    assert response.status_code == 401


# ---------------------------------------------------------
# Admin can access admin endpoint
# ---------------------------------------------------------

def test_admin_can_access_admin_endpoint():

    token = create_access_token(
        {
            "sub": "1",
            "username": "admin",
            "role": "admin",
        }
    )

    response = client.get(
        "/admin/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Welcome to the admin dashboard."
    )

    assert data["user"]["role"] == "admin"


# ---------------------------------------------------------
# Student cannot access admin endpoint
# ---------------------------------------------------------

def test_student_cannot_access_admin_endpoint():

    token = create_access_token(
        {
            "sub": "2",
            "username": "student",
            "role": "student",
        }
    )

    response = client.get(
        "/admin/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403

    assert response.json()["detail"] == (
        "Administrator access required."
    )


# ---------------------------------------------------------
# Invalid token cannot access admin endpoint
# ---------------------------------------------------------

def test_invalid_token_cannot_access_admin_endpoint():

    response = client.get(
        "/admin/dashboard",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


# ---------------------------------------------------------
# No token cannot access admin endpoint
# ---------------------------------------------------------

def test_no_token_cannot_access_admin_endpoint():

    response = client.get(
        "/admin/dashboard"
    )

    assert response.status_code == 401
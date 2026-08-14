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
# Student registration
# ---------------------------------------------------------

def test_student_can_register():

    username = "register_test_user"

    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "RegisterPassword123!",
            "student_number": "REG-STU-001",
            "name": "Registration Test Student",
            "email": "register.test@example.com",
            "department": "Computer Science",
            "level": 300,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] is not None
    assert data["student_id"] is not None
    assert data["username"] == username
    assert data["role"] == "student"
    assert data["student_number"] == "REG-STU-001"
    assert data["name"] == "Registration Test Student"
    assert data["email"] == "register.test@example.com"
    assert data["department"] == "Computer Science"
    assert data["level"] == 300

    delete_test_user(username)


def test_registered_student_password_is_hashed():

    username = "register_hash_user"

    try:
        response = client.post(
            "/auth/register",
            json={
                "username": username,
                "password": "RegisterPassword123!",
                "student_number": "REG-HASH-001",
                "name": "Hash Test Student",
                "email": "register.hash@example.com",
                "department": "Computer Science",
                "level": 200,
            },
        )

        assert response.status_code == 201

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
            "RegisterPassword123!"
        )

        assert password_hash.startswith("$2")

    finally:
        delete_test_user(username)


def test_registered_student_can_login():

    username = "register_login_user"
    password = "RegisterPassword123!"

    try:
        registration_response = client.post(
            "/auth/register",
            json={
                "username": username,
                "password": password,
                "student_number": "REG-LOGIN-001",
                "name": "Registration Login Student",
                "email": "register.login@example.com",
                "department": "Computer Science",
                "level": 300,
            },
        )

        assert registration_response.status_code == 201

        login_response = client.post(
            "/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        data = login_response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["access_token"]

    finally:
        delete_test_user(username)


def test_duplicate_username_registration_is_rejected():

    username = "duplicate_register_user"

    try:
        first_response = client.post(
            "/auth/register",
            json={
                "username": username,
                "password": "RegisterPassword123!",
                "student_number": "REG-DUP-001",
                "name": "First Student",
                "email": "duplicate.first@example.com",
                "department": "Computer Science",
                "level": 300,
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/auth/register",
            json={
                "username": username,
                "password": "AnotherPassword123!",
                "student_number": "REG-DUP-002",
                "name": "Second Student",
                "email": "duplicate.second@example.com",
                "department": "Computer Science",
                "level": 300,
            },
        )

        assert second_response.status_code == 409

    finally:
        delete_test_user(username)


def test_duplicate_student_number_registration_is_rejected():

    username_1 = "duplicate_student_number_1"
    username_2 = "duplicate_student_number_2"

    try:
        first_response = client.post(
            "/auth/register",
            json={
                "username": username_1,
                "password": "RegisterPassword123!",
                "student_number": "REG-SAME-001",
                "name": "First Student",
                "email": "same.number.first@example.com",
                "department": "Computer Science",
                "level": 300,
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/auth/register",
            json={
                "username": username_2,
                "password": "RegisterPassword123!",
                "student_number": "REG-SAME-001",
                "name": "Second Student",
                "email": "same.number.second@example.com",
                "department": "Computer Science",
                "level": 300,
            },
        )

        assert second_response.status_code == 409

    finally:
        delete_test_user(username_1)
        delete_test_user(username_2)


def test_duplicate_email_registration_is_rejected():

    username_1 = "duplicate_email_1"
    username_2 = "duplicate_email_2"

    try:
        first_response = client.post(
            "/auth/register",
            json={
                "username": username_1,
                "password": "RegisterPassword123!",
                "student_number": "REG-EMAIL-001",
                "name": "First Student",
                "email": "same.email@example.com",
                "department": "Computer Science",
                "level": 300,
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/auth/register",
            json={
                "username": username_2,
                "password": "RegisterPassword123!",
                "student_number": "REG-EMAIL-002",
                "name": "Second Student",
                "email": "same.email@example.com",
                "department": "Computer Science",
                "level": 300,
            },
        )

        assert second_response.status_code == 409

    finally:
        delete_test_user(username_1)
        delete_test_user(username_2)

def test_registration_with_invalid_email_is_rejected():

    response = client.post(
        "/auth/register",
        json={
            "username": "invalid_email_user",
            "password": "RegisterPassword123!",
            "student_number": "REG-INVALID-001",
            "name": "Invalid Email Student",
            "email": "not-an-email",
            "department": "Computer Science",
            "level": 300,
        },
    )

    assert response.status_code == 422


def test_registration_with_short_password_is_rejected():

    response = client.post(
        "/auth/register",
        json={
            "username": "short_password_user",
            "password": "short",
            "student_number": "REG-SHORT-001",
            "name": "Short Password Student",
            "email": "short.password@example.com",
            "department": "Computer Science",
            "level": 300,
        },
    )

    assert response.status_code == 422


def test_registration_with_invalid_level_is_rejected():

    response = client.post(
        "/auth/register",
        json={
            "username": "invalid_level_user",
            "password": "RegisterPassword123!",
            "student_number": "REG-LEVEL-001",
            "name": "Invalid Level Student",
            "email": "invalid.level@example.com",
            "department": "Computer Science",
            "level": 0,
        },
    )

    assert response.status_code == 422        


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

def test_registration_creates_user_and_student_profile():

    username = "registration_database_user"

    try:
        response = client.post(
            "/auth/register",
            json={
                "username": username,
                "password": "RegisterPassword123!",
                "student_number": "REG-DB-001",
                "name": "Database Registration Student",
                "email": "registration.database@example.com",
                "department": "Computer Science",
                "level": 400,
            },
        )

        assert response.status_code == 201

        data = response.json()

        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, username, role
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        user = cursor.fetchone()

        cursor.execute(
            """
            SELECT id, user_id, student_number, name
            FROM students
            WHERE student_number = ?
            """,
            ("REG-DB-001",),
        )

        student = cursor.fetchone()

        connection.close()

        assert user is not None
        assert student is not None

        assert user[0] == data["user_id"]
        assert student[0] == data["student_id"]

        assert student[1] == user[0]
        assert user[2] == "student"

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
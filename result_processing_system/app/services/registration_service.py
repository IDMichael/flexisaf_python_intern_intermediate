import sqlite3

from app.core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
)
from app.core.security import hash_password
from app.database.connection import create_connection


def register_student(
    username,
    password,
    student_number,
    name,
    email,
    department,
    level,
):
    """Create a student user account and student profile."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        # -------------------------------------------------
        # Check username
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        if cursor.fetchone() is not None:
            raise DuplicateResourceError(
                "Username"
            )

        # -------------------------------------------------
        # Check student number
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE student_number = ?
            """,
            (student_number,),
        )

        if cursor.fetchone() is not None:
            raise DuplicateResourceError(
                "Student number"
            )

        # -------------------------------------------------
        # Check email
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE email = ?
            """,
            (email,),
        )

        if cursor.fetchone() is not None:
            raise DuplicateResourceError(
                "Email"
            )

        # -------------------------------------------------
        # Hash password
        # -------------------------------------------------

        password_hash = hash_password(password)

        # -------------------------------------------------
        # Create user account
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                role,
                is_active
            )
            VALUES (?, ?, 'student', 1)
            """,
            (
                username,
                password_hash,
            ),
        )

        user_id = cursor.lastrowid

        # -------------------------------------------------
        # Create student profile
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO students (
                user_id,
                student_number,
                name,
                email,
                department,
                level
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                student_number,
                name,
                email,
                department,
                level,
            ),
        )

        student_id = cursor.lastrowid

        connection.commit()

        return {
            "user_id": user_id,
            "student_id": student_id,
            "username": username,
            "role": "student",
            "student_number": student_number,
            "name": name,
            "email": email,
            "department": department,
            "level": level,
        }

    except DuplicateResourceError:
        connection.rollback()
        raise

    except sqlite3.IntegrityError as error:
        connection.rollback()

        raise DuplicateResourceError(
            "Student registration"
        ) from error

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()
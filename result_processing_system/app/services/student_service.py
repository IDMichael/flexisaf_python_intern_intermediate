import sqlite3

from app.core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
    ResourceNotFoundError,
)
from app.database.connection import create_connection


def create_student(
    student_number,
    name,
    email,
    department,
    level,
):
    """Create a student."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students (
                student_number,
                name,
                email,
                department,
                level
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_number,
                name,
                email,
                department,
                level,
            ),
        )

        student_id = cursor.lastrowid

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                student_number,
                name,
                email,
                department,
                level
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        )

        return cursor.fetchone()

    except sqlite3.IntegrityError as error:
        connection.rollback()

        raise DuplicateResourceError(
            "Student"
        ) from error

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()


def get_student_by_id(student_id):
    """Get one student by ID."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                student_number,
                name,
                email,
                department,
                level,
                created_at,
                updated_at
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        )

        student = cursor.fetchone()

        if student is None:
            raise ResourceNotFoundError(
                "Student"
            )

        return student

    except ResourceNotFoundError:
        raise

    except sqlite3.Error as error:
        raise DatabaseError() from error

    finally:
        connection.close()


def update_student(
    student_id,
    student_number,
    name,
    email,
    department,
    level,
):
    """Update an existing student."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        )

        if cursor.fetchone() is None:
            raise ResourceNotFoundError(
                "Student"
            )

        # Check whether another student already uses
        # the submitted student number.
        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE student_number = ?
            AND id != ?
            """,
            (student_number, student_id),
        )

        if cursor.fetchone() is not None:
            raise DuplicateResourceError(
                "Student"
            )

        # Check whether another student already exists
        # the submitted email.
        if email is not None:
            cursor.execute(
                """
                SELECT id
                FROM students
                WHERE email = ?
                AND id != ?
                """,
                (email, student_id),
            )  

        if cursor.fetchone() is not None:
            raise DuplicateResourceError(
                "Student"
            )

        # Update the student.
        cursor.execute(
            """
            UPDATE students
            SET
                student_number = ?,
                name = ?,
                email = ?,
                department = ?,
                level = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                student_number,
                name,
                email,
                department,
                level,
                student_id,
            ),
        )

        connection.commit()

        # Retrieve the updated student. 
        cursor.execute(
            """
            SELECT
                id,
                student_number,
                name,
                email,
                department,
                level
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        )

        return cursor.fetchone()

    except ResourceNotFoundError:
        connection.rollback()
        raise

    except DuplicateResourceError:
        connection.rollback()
        raise

        raise DuplicateResourceError(
            "Student"
        ) from error

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()


def delete_student(student_id):
    """Delete a student by ID."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE id = ?
            """,
            (student_id,),
        )

        if cursor.fetchone() is None:
            raise ResourceNotFoundError(
                "Student"
            )

        cursor.execute(
            """
            DELETE FROM students
            WHERE id = ?
            """,
            (student_id,),
        )

        connection.commit()

    except ResourceNotFoundError:
        connection.rollback()
        raise

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()
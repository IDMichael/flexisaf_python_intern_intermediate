import sqlite3

from app.core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
    ResourceNotFoundError,
)
from app.database.connection import create_connection


def create_result(
    student_id,
    course_id,
    score,
    semester,
    session,
):
    """Create a student result."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,),
        )

        if cursor.fetchone() is None:
            raise ResourceNotFoundError("Student")

        cursor.execute(
            "SELECT id FROM courses WHERE id = ?",
            (course_id,),
        )

        if cursor.fetchone() is None:
            raise ResourceNotFoundError("Course")

        cursor.execute(
            """
            INSERT INTO results (
                student_id,
                course_id,
                score,
                semester,
                session
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_id,
                course_id,
                score,
                semester,
                session,
            ),
        )

        result_id = cursor.lastrowid

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                student_id,
                course_id,
                score,
                semester,
                session
            FROM results
            WHERE id = ?
            """,
            (result_id,),
        )

        return cursor.fetchone()

    except ResourceNotFoundError:
        connection.rollback()
        raise

    except sqlite3.IntegrityError as error:
        connection.rollback()

        raise DuplicateResourceError(
            "Result"
        ) from error

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()

def get_result_by_id(result_id):
    """Get one result by ID."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                results.id,
                results.student_id,
                results.course_id,
                results.score,
                results.semester,
                results.session
            FROM results
            WHERE results.id = ?
            """,
            (result_id,),
        )

        result = cursor.fetchone()

        if result is None:
            raise ResourceNotFoundError(
                "Result"
            )

        return result

    except ResourceNotFoundError:
        raise

    except sqlite3.Error as error:
        raise DatabaseError() from error

    finally:
        connection.close()


def update_result(
    result_id,
    student_id,
    course_id,
    score,
    semester,
    session,
):
    """Update an existing result."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM results
            WHERE id = ?
            """,
            (result_id,),
        )

        if cursor.fetchone() is None:
            raise ResourceNotFoundError(
                "Result"
            )

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
            SELECT id
            FROM courses
            WHERE id = ?
            """,
            (course_id,),
        )

        if cursor.fetchone() is None:
            raise ResourceNotFoundError(
                "Course"
            )

        cursor.execute(
            """
            UPDATE results
            SET
                student_id = ?,
                course_id = ?,
                score = ?,
                semester = ?,
                session = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                student_id,
                course_id,
                score,
                semester,
                session,
                result_id,
            ),
        )

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                student_id,
                course_id,
                score,
                semester,
                session
            FROM results
            WHERE id = ?
            """,
            (result_id,),
        )

        return cursor.fetchone()

    except ResourceNotFoundError:
        connection.rollback()
        raise

    except sqlite3.IntegrityError as error:
        connection.rollback()

        raise DuplicateResourceError(
            "Result"
        ) from error

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()


def delete_result(result_id):
    """Delete a result."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM results
            WHERE id = ?
            """,
            (result_id,),
        )

        if cursor.fetchone() is None:
            raise ResourceNotFoundError(
                "Result"
            )

        cursor.execute(
            """
            DELETE FROM results
            WHERE id = ?
            """,
            (result_id,),
        )

        connection.commit()

        return True

    except ResourceNotFoundError:
        connection.rollback()
        raise

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()
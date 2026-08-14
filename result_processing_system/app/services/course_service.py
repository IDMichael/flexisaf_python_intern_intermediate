import sqlite3

from app.core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
    ResourceNotFoundError,
)

from app.database.connection import create_connection


def create_course(
    course_code,
    course_name,
    credit_unit,
):
    """Create a course."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO courses (
                course_code,
                course_name,
                credit_unit
            )
            VALUES (?, ?, ?)
            """,
            (
                course_code,
                course_name,
                credit_unit,
            ),
        )

        course_id = cursor.lastrowid

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                course_code,
                course_name,
                credit_unit
            FROM courses
            WHERE id = ?
            """,
            (course_id,),
        )

        return cursor.fetchone()

    except sqlite3.IntegrityError as error:
        connection.rollback()

        raise DuplicateResourceError(
            "Course"
        ) from error

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()


def get_course_by_id(course_id):
    """Get one course by ID."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                course_code,
                course_name,
                credit_unit,
                created_at,
                updated_at
            FROM courses
            WHERE id = ?
            """,
            (course_id,),
        )

        course = cursor.fetchone()

        if course is None:
            raise ResourceNotFoundError(
                "Course"
            )

        return course

    except ResourceNotFoundError:
        raise

    except sqlite3.Error as error:
        raise DatabaseError() from error

    finally:
        connection.close()


def update_course(
    course_id,
    course_code,
    course_name,
    credit_unit,
):
    """Update a course."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

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
            UPDATE courses
            SET
                course_code = ?,
                course_name = ?,
                credit_unit = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                course_code,
                course_name,
                credit_unit,
                course_id,
            ),
        )

        connection.commit()

        cursor.execute(
            """
            SELECT
                id,
                course_code,
                course_name,
                credit_unit
            FROM courses
            WHERE id = ?
            """,
            (course_id,),
        )

        return cursor.fetchone()

    except ResourceNotFoundError:
        connection.rollback()
        raise

    except sqlite3.IntegrityError as error:
        connection.rollback()

        raise DuplicateResourceError(
            "Course"
        ) from error

    except sqlite3.Error as error:
        connection.rollback()

        raise DatabaseError() from error

    finally:
        connection.close()


def delete_course(course_id):
    """Delete a course."""

    connection = create_connection()

    if connection is None:
        raise DatabaseError()

    try:
        cursor = connection.cursor()

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
            DELETE FROM courses
            WHERE id = ?
            """,
            (course_id,),
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
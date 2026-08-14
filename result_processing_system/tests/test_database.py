import sqlite3

import pytest


@pytest.fixture
def connection():
    """Create an isolated in-memory database for testing."""

    connection = sqlite3.connect(":memory:")

    # Enable foreign key enforcement.
    connection.execute("PRAGMA foreign_keys = ON")

    cursor = connection.cursor()

    # Create students table.
    cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            department TEXT NOT NULL,
            level INTEGER NOT NULL,

            CHECK (length(trim(name)) > 0),
            CHECK (length(trim(student_number)) > 0),
            CHECK (level > 0)
        )
    """)

    # Create courses table.
    cursor.execute("""
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            credit_unit INTEGER NOT NULL,

            CHECK (length(trim(course_code)) > 0),
            CHECK (length(trim(course_name)) > 0),
            CHECK (credit_unit > 0)
        )
    """)

    # Create results table.
    cursor.execute("""
        CREATE TABLE results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,

            score REAL NOT NULL,

            semester TEXT NOT NULL,
            session TEXT NOT NULL,

            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE,

            FOREIGN KEY (course_id)
                REFERENCES courses(id)
                ON DELETE CASCADE,

            CHECK (score >= 0 AND score <= 100),
            CHECK (length(trim(semester)) > 0),
            CHECK (length(trim(session)) > 0),

            UNIQUE (
                student_id,
                course_id,
                semester,
                session
            )
        )
    """)

    connection.commit()

    yield connection

    connection.close()


def test_database_connection(connection):
    """Verify that the database connection works."""

    cursor = connection.cursor()

    cursor.execute("SELECT 1")

    result = cursor.fetchone()

    assert result == (1,)


def test_students_table_exists(connection):
    """Verify that the students table exists."""

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'students'
    """)

    result = cursor.fetchone()

    assert result == ("students",)


def test_courses_table_exists(connection):
    """Verify that the courses table exists."""

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'courses'
    """)

    result = cursor.fetchone()

    assert result == ("courses",)


def test_results_table_exists(connection):
    """Verify that the results table exists."""

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'results'
    """)

    result = cursor.fetchone()

    assert result == ("results",)


def test_student_can_be_inserted(connection):
    """Verify that a valid student can be inserted."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (
            student_number,
            name,
            email,
            department,
            level
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        "STU001",
        "John Doe",
        "john@example.com",
        "Computer Science",
        300
    ))

    connection.commit()

    cursor.execute("""
        SELECT student_number, name
        FROM students
        WHERE student_number = ?
    """, ("STU001",))

    result = cursor.fetchone()

    assert result == ("STU001", "John Doe")


def test_course_can_be_inserted(connection):
    """Verify that a valid course can be inserted."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO courses (
            course_code,
            course_name,
            credit_unit
        )
        VALUES (?, ?, ?)
    """, (
        "CSC301",
        "Database Systems",
        3
    ))

    connection.commit()

    cursor.execute("""
        SELECT course_code, course_name, credit_unit
        FROM courses
        WHERE course_code = ?
    """, ("CSC301",))

    result = cursor.fetchone()

    assert result == (
        "CSC301",
        "Database Systems",
        3
    )


def test_result_can_be_inserted(connection):
    """Verify that a valid result can be inserted."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (
            student_number,
            name,
            department,
            level
        )
        VALUES (?, ?, ?, ?)
    """, (
        "STU001",
        "John Doe",
        "Computer Science",
        300
    ))

    cursor.execute("""
        INSERT INTO courses (
            course_code,
            course_name,
            credit_unit
        )
        VALUES (?, ?, ?)
    """, (
        "CSC301",
        "Database Systems",
        3
    ))

    student_id = cursor.lastrowid

    cursor.execute("""
        SELECT id
        FROM courses
        WHERE course_code = ?
    """, ("CSC301",))

    course_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO results (
            student_id,
            course_id,
            score,
            semester,
            session
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        student_id,
        course_id,
        80,
        "First",
        "2025/2026"
    ))

    connection.commit()

    cursor.execute("""
        SELECT score
        FROM results
        WHERE student_id = ?
        AND course_id = ?
    """, (student_id, course_id))

    result = cursor.fetchone()

    assert result == (80.0,)


def test_score_above_100_is_rejected(connection):
    """Verify that scores above 100 are rejected."""

    cursor = connection.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO students (
                student_number,
                name,
                department,
                level
            )
            VALUES (?, ?, ?, ?)
        """, (
            "STU001",
            "John Doe",
            "Computer Science",
            300
        ))

        student_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO courses (
                course_code,
                course_name,
                credit_unit
            )
            VALUES (?, ?, ?)
        """, (
            "CSC301",
            "Database Systems",
            3
        ))

        course_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO results (
                student_id,
                course_id,
                score,
                semester,
                session
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            student_id,
            course_id,
            101,
            "First",
            "2025/2026"
        ))


def test_negative_score_is_rejected(connection):
    """Verify that negative scores are rejected."""

    cursor = connection.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO students (
                student_number,
                name,
                department,
                level
            )
            VALUES (?, ?, ?, ?)
        """, (
            "STU001",
            "John Doe",
            "Computer Science",
            300
        ))

        student_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO courses (
                course_code,
                course_name,
                credit_unit
            )
            VALUES (?, ?, ?)
        """, (
            "CSC301",
            "Database Systems",
            3
        ))

        course_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO results (
                student_id,
                course_id,
                score,
                semester,
                session
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            student_id,
            course_id,
            -1,
            "First",
            "2025/2026"
        ))


def test_duplicate_student_number_is_rejected(connection):
    """Verify that student numbers must be unique."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (
            student_number,
            name,
            department,
            level
        )
        VALUES (?, ?, ?, ?)
    """, (
        "STU001",
        "John Doe",
        "Computer Science",
        300
    ))

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO students (
                student_number,
                name,
                department,
                level
            )
            VALUES (?, ?, ?, ?)
        """, (
            "STU001",
            "Jane Doe",
            "Computer Science",
            300
        ))


def test_duplicate_course_code_is_rejected(connection):
    """Verify that course codes must be unique."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO courses (
            course_code,
            course_name,
            credit_unit
        )
        VALUES (?, ?, ?)
    """, (
        "CSC301",
        "Database Systems",
        3
    ))

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO courses (
                course_code,
                course_name,
                credit_unit
            )
            VALUES (?, ?, ?)
        """, (
            "CSC301",
            "Advanced Database Systems",
            3
        ))


def test_invalid_credit_unit_is_rejected(connection):
    """Verify that zero or negative credit units are rejected."""

    cursor = connection.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO courses (
                course_code,
                course_name,
                credit_unit
            )
            VALUES (?, ?, ?)
        """, (
            "CSC301",
            "Database Systems",
            0
        ))


def test_nonexistent_student_is_rejected(connection):
    """Verify that results cannot reference nonexistent students."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO courses (
            course_code,
            course_name,
            credit_unit
        )
        VALUES (?, ?, ?)
    """, (
        "CSC301",
        "Database Systems",
        3
    ))

    course_id = cursor.lastrowid

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO results (
                student_id,
                course_id,
                score,
                semester,
                session
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            999,
            course_id,
            80,
            "First",
            "2025/2026"
        ))


def test_duplicate_result_is_rejected(connection):
    """Verify that duplicate student-course results are rejected."""

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (
            student_number,
            name,
            department,
            level
        )
        VALUES (?, ?, ?, ?)
    """, (
        "STU001",
        "John Doe",
        "Computer Science",
        300
    ))

    student_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO courses (
            course_code,
            course_name,
            credit_unit
        )
        VALUES (?, ?, ?)
    """, (
        "CSC301",
        "Database Systems",
        3
    ))

    course_id = cursor.lastrowid

    result_data = (
        student_id,
        course_id,
        80,
        "First",
        "2025/2026"
    )

    cursor.execute("""
        INSERT INTO results (
            student_id,
            course_id,
            score,
            semester,
            session
        )
        VALUES (?, ?, ?, ?, ?)
    """, result_data)

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO results (
                student_id,
                course_id,
                score,
                semester,
                session
            )
            VALUES (?, ?, ?, ?, ?)
        """, result_data)
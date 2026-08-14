import sqlite3
from app.database.connection import create_connection

# Create all application database tables.
def create_tables():

    connection = None
    cursor = None

    try:
        # Create a database connection
        connection = create_connection()

        if connection is None:
            return

        # Create a cursor for the exection of SQL commands.
        cursor = connection.cursor()

        # Create users table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                role TEXT NOT NULL DEFAULT 'student',

                is_active INTEGER NOT NULL DEFAULT 1,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                CHECK (
                    role IN (
                        'admin',
                        'lecturer',
                        'student'
                    )
                ),

                CHECK (
                    is_active IN (0, 1)
                )
            )
        """)

        # Create students table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            department TEXT NOT NULL,
            level INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            CHECK (length(trim(name)) > 0),
            CHECK (length(trim(student_number)) > 0),
            CHECK (level > 0)
            )
        """)

        #  Create courses table.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        course_code TEXT NOT NULL UNIQUE,
        credit_unit INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        CHECK (length(trim(course_code)) > 0),
        CHECK (length(trim(course_name)) > 0),
        CHECK (credit_unit > 0)
        )
        """)

        # Create results table.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,

        score REAL NOT NULL,

        semester TEXT NOT NULL,
        session TEXT NOT NULL,
        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (student_id)
            REFERENCES students(id)
            ON DELETE CASCADE,

        FOREIGN KEY (course_id)
            REFERENCES courses(id)
            ON DELETE CASCADE,

        CHECK (score >= 0 AND score <= 100),
        CHECK (length(trim(semester)) > 0),
        CHECK (length(trim(session)) > 0),

        unique(
            student_id,
            course_id,
            semester,
            session
            )
        )
        """)

        # Create indexes for frequently searched columns.\
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_students_department
            ON students(department)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_results_student
            ON results(student_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_results_course
            ON results(course_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_results_session
            ON results(session)
        """)

        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Table error: {error}")
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
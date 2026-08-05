import sqlite3

# SQLite database file name.
DATABASE_NAME = "students.db"

# Create and return a connection to the SQLite database.
def create_connection():
    connection = None

    try:
        # Connect to the SQLite database.
        connection = sqlite3.connect("DATABASE_NAME")

        # Enable foreign support.
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
        
    except sqlite3.Error as error:
        print("Database connection error: {error}")
        return None

# Create the database tables and indexes.
def create_tables():
    connection = None
    cursor = None

    try:
        # Create a database connection.
        connection = create_connection()

        if connection is None:
            return

        # Create a cursor for the execution of SQL commands.
        cursor = connection.cursor()

        # Student table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            department TEXT NOT NULL
            )
        """)

        # Create the logs table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            action TEXT NOT NULL,
            description NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY(student_id)
                REFERENCES students(id)
                ON DELETE SET NULL
            )
        """)

        # Create index for faster student name searchers.
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_name 
            ON students(name)
        """)

        # Create index for faster department searchers.
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_student_department
            ON students(department)
        """)

        # Create an index for faster log date sorting.
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_created_at
            ON logs(created_at)
        """)

        # Save all changes.
        connection.commit()

        print("Database tables and indexes created successfully!")

    except sqlite3.Error as error:
        print(f"Database error {error}")

    finally:
        # Close the cursor.
        if cursor:
            cursor.close()

        # Close the database connection.
        if connection:
            connection.close()

# Display SQLite's query plan.
def explain_query_plan():

    connection = None
    cursor = None

    try:
        # Create a database connection.
        connection = create_connection()

        if connection is None:
            return

        # Create a cursor.
        cursor = connection.cursor()

        # Ask SQLite how it plans to execute this query.
        cursor.execute("""
            EXPLAIN QUERY PLAN
            SELECT id, name, age, department
            FROM students
            WHERE department = ?
        """, ("Computer Science",))

        print("\n============ QUERY PLAN ===========")

        for row in cursor.fetchall():
            print(row)

    except sqlite3.Error as error:
        print(f"Query plan error: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
   
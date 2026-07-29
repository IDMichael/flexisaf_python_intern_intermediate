import sqlite3

# Database file name
DATABASE_NAME = "students.db"

# Create and return a connection to the SQLITE database
def create_connection():

    try:
        connection = sqlite3.connect(DATABASE_NAME)
        return connection
    
    except sqlite3.Error as error:
        print(f"Error: {error}")
        return None

# Create the students table if it doesn't already exists
def create_table():
    connection = None
    cursor = None

    try:
        # Create a database connection.
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor.
        cursor = connection.cursor()

        # Create a table for records in the database.
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    department TEXT NOT NULL)
            """)

        # Save changes to the database.
        connection.commit()
        print("Table created successfully!")

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if cursor:
            cursor.close() 

        if connection:
            connection.close()

# Create the logs table for recording database activities.
def create_logs():
    connection = None
    cursor = None

    try:
        # Create a database connection.
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor.
        cursor = connection.cursor()

        # Create the logs table if it does not already exist. 
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)

        # Save the table creation to the database.
        connection.commit()
        print("Logs table created successfully!")

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if cursor:
            cursor.close()
        
        if connection:
            connection.close()






 
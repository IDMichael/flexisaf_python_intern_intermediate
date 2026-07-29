import sqlite3
from database import create_connection

# Insert a new student into the database.
def add_student(name, age, department):
    cursor = None
    connection = None

    try:
        # Create a database connection
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor for executing SQL commands.
        cursor = connection.cursor()

        # SQL query to record the student creation in the logs table.
        insert_query = ("""
            INSERT INTO students(name, age, department)
            VALUES (?, ?, ?)
        """)

        # Log details describing the student creation.
        insert_values = (name, age, department)

        # Execute the INSERT statement.
        cursor.execute(insert_query, insert_values)

        # SQL query to insert new log
        insert_log = ("""
            INSERT INTO logs(action, description)
            VALUES (?, ?)
        """)

        # Values to insert into the logs
        values_logs = (
            "CREATE",
            f"Added student '{name}' to {department}"
            )
        
        cursor.execute(insert_log, values_logs)

        # Save both the student record and the log entry.
        connection.commit()
        print("Student data inserted successfully!")

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor and database connection.
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# Display all students.
def view_students():
    cursor = None
    connection = None

    try:
        # Create a database connection.
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor.
        cursor = connection.cursor()

        # Retrieve all the student records.
        cursor.execute("SELECT * FROM students")

        # Retrieve all student records from the query result.
        students = cursor.fetchall()
        if not students:
            print("No students found.")
            return
        
        print("\n                        Students")
        print("=" * 60)

        for student in students:
            print(student)

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor and database connection.
        if cursor:
            cursor.close()
        
        if connection:
            connection.close()

# Display all activity logs.
def view_logs():
    connection = None
    cursor = None

    try:
        # Create a databse connection.
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor for executing SQL commands.
        cursor = connection.cursor()

        # Retrieve all logs, showing the newest entries first.
        cursor.execute("""
            SELECT * FROM logs
            ORDER BY created_at DESC
        """)

        # Store all log records.
        logs = cursor.fetchall()

        # Check whether any logs exist.
        if not logs:
            print("No logs found.")
            return

        print("\n                                  ==== ACTIVITY LOGS ====")
        print("=" * 90)        

        # Display each log entry.
        for log in logs:
            print(f"""
            ID: {log[0]}
            ACTION: {(log[1])}
            DESCRIPTION: {(log[2])}
            DATE: {(log[3])}
            {"-" * 70}
            """)

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

# Update a student's department.
def update_student(student_id, new_department):
    cursor = None
    connection = None

    try:
        # Create a database connection.
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor for the execution of SQL commands.
        cursor = connection.cursor()

        # SQL query to update a student's department.
        update_query = ("""
            UPDATE students
            SET department = ?
            WHERE id = ?
        """)

        # Values for the UPDATE statement.
        update_values = (new_department, student_id)

        cursor.execute(update_query, update_values)

        # Check whether any row was updated.
        if cursor.rowcount == 0:
            print("Student not found.")

        else:
            # Record the update in the logs table.
            insert_log = """
                INSERT INTO logs(action, description)
                VALUES (?, ?)
            """

            values_log = (
                "UPDATE",
                f"Updated student ID {student_id} department to '{new_department}'."
            )

            cursor.execute(insert_log, values_log)

            # Save both the update and the log entry.
            connection.commit()

            print("Student updated successfully!")

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

# Delete a student by ID.
def delete_student(student_id):
    cursor = None
    connection = None
    
    try:
        # Create a database connection.
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor for the execution SQL commands.
        cursor = connection.cursor()

        # SQL query to retrieve the student's name before deletion.
        select_query = ("SELECT name FROM students WHERE id = ?")

        # Value used to find the student record.
        delete_values = (student_id,)

        # Execute the delete statement.
        cursor.execute(select_query, delete_values)

        # Store the student's details.
        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            return

        # SQL query to delete the student record.
        delete_query = """
            DELETE FROM students 
            WHERE id = ?
        """

        # Execute the DELETE statement.
        cursor.execute(delete_query, delete_values)

        # SQL query to insert the deletion in the logs table.
        insert_log = """
            INSERT INTO logs(action, description)
            VALUES (?, ?)
        """

        # Details about the deletion activity.
        values_logs = (
            "DELETE",
            f"Deleted student '{student[0]}' (ID {student_id})."
        )

        # Savae the deletion activity into the logs table.
        cursor.execute(insert_log, values_logs)

        # Save both the deletion and the log entry permanently.
        connection.commit()

        print("Student deleted successfully!")

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor and the database connection.
        if cursor:
            cursor.close()
        
        if connection:
            connection.close()
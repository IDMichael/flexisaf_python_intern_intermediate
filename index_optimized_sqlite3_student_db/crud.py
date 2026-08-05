import sqlite3
from database import create_connection

# Add a new student.
def add_student(name, age, department):

    connection = None
    cursor = None

    try:
        # Create a database connection
        connection = create_connection()

        if connection is None:
            return

        # Create a cursor for the execution of SQL commands.
        cursor = connection.cursor()

        # Start a transaction.
        connection.execute("BEGIN")

        # SQL statement to insert a new student.
        insert_student = """
            INSERT INTO students(name, age, department)
            VALUES (?, ?, ?)
        """

        cursor.execute(
            insert_student,
            (name, age, department)
        )

        # Get the ID of the newly inserted student.
        student_id = cursor.lastrowid

        # Record the activity in the logs table.
        insert_log = """
            INSERT INTO logs(student_id, action, description)
            VALUES (?, ?, ?)
        """

        cursor.execute(
            insert_log,
            (student_id,
             "CREATE",
             f"Added student '{name}' to '{department}'.")
        )

        # Save both operations.
        connection.commit()

        print("Student added successfully!")

    except sqlite3.Error as error:
        print(f"Error: {error}")

        # Undo every operation if an error occurs.
        if connection:
            connection.rollback()

        print(f"Error: {error}")

    finally:

        if cursor:
            cursor.connection

        if connection:
            connection.close()

# Display all students.
def view_students():

    connection = None
    cursor = None

    try:
        # Create a database connection
        connection = create_connection()

        if connection is None:
            return

        # Create a cursor for the execution of SQL commands.
        cursor = connection.cursor()

        # Select only the required columns.
        cursor.execute("""
            SELECT id, name, age, department
            FROM students
            ORDER BY name ASC
        """)

        students = cursor.fetchall()

        if not students:
            print("No students found.")
            return

        print("\n==================== STUDENTS ====================")

        for student in students:
            print(f"""
ID          : {student[0]}
Name        : {student[1]}
Age         : {student[2]}
Department  : {student[3]}
{"-" * 50}
""")
    except sqlite3.Error as error:
        print(f"Error {error}")

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# Search students by name.
def search_student(name):

    connection = None
    cursor = None

    try:
        # Create a database connection.
        connection = create_connection()

        # Stop if the connection failed.
        if connection is None:
            return

        # Create a cursor for executing SQL commands.
        cursor = connection.cursor()

        # Search for students whose names contain the
        # text entered by the user.
        cursor.execute("""
            SELECT id, name, age, department
            FROM students
            WHERE name LIKE ?
            ORDER BY name ASC
        """, (f"%{name}%",))

        # Retrieve all matching student records.
        students = cursor.fetchall()

        # Check whether any matching students were found.
        if not students:
            print("No matching students found.")
            return

        # Display the search results heading.
        print("\n========================== SEARCH RESULTS ==========================\n")

        # Display each matching student.
        for student in students:
            print(f"""
ID          : {student[0]}
Name        : {student[1]}
Age         : {student[2]}
Department  : {student[3]}
{"-" * 50}
""")

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        # Close the cursor and database connection.
        if cursor:
            cursor.close()

        if connection:
            connection.close()

# Display SQLite's query plandef explain_department_search():
def explain_department_search():

    connection = None
    cursor = None

    try:
        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        department = input("Enter department to analyze: ").strip()

        if not department:
            print("Department cannot be empty.")
            return

        cursor.execute("""
            EXPLAIN QUERY PLAN
            SELECT id, name, age, department
            FROM students
            WHERE department = ?
        """, (department,))

        print("\n================================= QUERY PLAN ===================================\n")

        for row in cursor.fetchall():
            print(row)

        # Execute the actual query.
        cursor.execute("""
            SELECT id, name, age, department
            FROM students
            WHERE department = ?
        """, (department,))

        students = cursor.fetchall()

        print("\n=================================== RESULTS ====================================\n")

        if not students:
             print("No students found.")

        else:
            for student in students:
                print(student)

    except sqlite3.Error as error:
        print(f"Error: {error}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

# Display all activity logs.
def view_logs():

	connection = None
	cursor = None

	try:
		# Create a database connection.
		connection = create_connection()

		# Create a cursor for the execution of SQL commands.
		cursor = connection.cursor()

		# Retrieve log entries together with the student's name.
		cursor.execute("""
			SELECT
				logs.id,
				students.name,
				logs.action,
				logs.description,
				logs.created_at
			FROM logs
			INNER JOIN students
			ON students.id = logs.student_id
			ORDER BY logs.created_at DESC
		""")

		logs = cursor.fetchall()

		if not logs:
			print("No logs found.")
			return

		print("\n================================ ACTIVITY LOGS ================================\n")

		for log in logs:
			print(f"{'Log ID':20}: {log[0]}")
			print(f"{'Student':20}: {log[1]}")
			print(f"{'Action':20}: {log[2]}")
			print(f"{'Description':20}: {log[3]}")
			print(f"{'Date':20}: {log[4]}")
			print("-" * 80)

	except sqlite3.Error as error:
		print(f"Error: {error}")

	finally:

		if cursor:
			cursor.close()

		if connection:
			connection.close()
               
# Update a student's department.
def update_student(student_id, new_department):

    connection = None
    cursor = None

    try:

        connection = create_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        # Start a transaction.
        connection.execute("BEGIN")

        # Check whether the student exists.
        cursor.execute("""
            SELECT
                name
            FROM students
            WHERE id = ?
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            connection.rollback()
            return

        # Update the department.
        cursor.execute("""
            UPDATE students
            SET department = ?
            WHERE id = ?
        """, (new_department, student_id))

        # Record the update in the logs table.
        cursor.execute("""
            INSERT INTO logs(
                student_id,
                action,
                description
            )
            VALUES (?, ?, ?)
        """,
        (
            student_id,
            "UPDATE",
            f"Updated {student[0]}'s department to '{new_department}'."
        ))

        # Save both operations.
        connection.commit()

        print("Student updated successfully.")

    except sqlite3.Error as error:

        if connection:
            connection.rollback()

        print(f"Error: {error}")

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# Delete a student.
def delete_student(student_id):

    connection = None
    cursor = None

    try:
          
        connection = create_connection()

        if connection is None:
            print("Database connection failed.")
            return

        # Create a cursor for executing SQL commands.
        cursor = connection.cursor()
        
        # Start a transaction.
        connection.execute("BEGIN")

        # Retrieve the student's name.
        cursor.execute("""
            SELECT name
            FROM students
            WHERE id = ?
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
             print(("Student not found."))
             connection.rollback()
             return

        # Delete the student.
        cursor.execute("""
        INSERT INTO logs(student_id, action, description)
        VALUES (?, ?, ?)
        """, (
             student_id,
             "DELETE",
             f"Deleted student '{student[0]}'."
        ))
        cursor.execute("""
            DELETE FROM students
            WHERE id = ?
            """, (student_id,))

        # Commit the transaction.
        connection.commit()

        print(f"Student '{student[0]}' deleted successfully.")

    except sqlite3.Error as error:

        if connection:
            connection.rollback()

        print(f"Error: {error}")

    finally:

        if cursor:
            cursor.close()

        if connection:
             connection.close()
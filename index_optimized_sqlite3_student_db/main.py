from database import create_tables
from crud import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student,
    view_logs,
    explain_department_search
)

# Display the application menu.
def menu():
    print("\n================= STUDENT DATABASE =================")
    print("1. Add Student")
    print("2. View Student")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. View Logs")
    print("7. Explain Query Plan")
    print("8. Exit")

def main():
    try:
        # Create the database tables and indexes.
        create_tables()

        while True:

            menu()

            choice = input("\nEnter your choice: ").strip()

            if not choice:
                print("Choice cannot be empty.")
                continue

            # Add Student
            if choice == "1":

                name = input("Student name: ").strip()

                if not name:
                    print("Name cannot be empty.")
                    continue

                try:
                    age = int(input("Age: "))

                    if age <= 0:
                        print("Age must be greater than zero.")
                        continue

                except ValueError:
                    print("Age must be greater than zero.")
                    continue

                department = input("Department: ").strip()

                if not department:
                    print("Department cannot be empty.")
                    continue

                add_student(name, age, department)

            # View Students
            elif choice == "2":
                view_students()

            # Search Student
            elif choice == "3":
                name = input("Enter student name: ").strip()

                if not name:
                    print("Name cannot be empty.")
                    continue

                search_student(name)

            # Update Student
            elif choice == "4":

                try:
                    student_id = int(input("Student ID: "))

                except ValueError:
                    print("Invalid student ID.")
                    continue

                department = input("New Department: ").strip()

                if not department:
                    print("Department cannot be empty.")
                    continue

                update_student(student_id, department)

            # Delete Student
            elif choice == "5":

                try:
                    student_id = int(input("Student ID: "))

                except ValueError:
                    print("Invalid student ID.")
                    continue

                delete_student(student_id)

            # View Logs
            elif choice == "6":
                view_logs()

            # Explain Query Plan
            elif choice == "7":
                explain_department_search()

            # Exit
            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Please, choose a valid option.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

if __name__ == "__main__":
    main()
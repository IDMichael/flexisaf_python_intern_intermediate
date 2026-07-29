from database import create_table, create_logs
from crud import (add_student, view_students, update_student, delete_student, view_logs)

# Display the application menu.
def menu():
    print("\n==== STUDENT DATABASE ====")
    print("1. Add Student")
    print("2. View Student")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. View Logs")
    print("6. Exit")

def main():
    try:
        # Create the required database tables before starting the application.
        create_table()
        create_logs()

        # Keep the application running until the user chooses to exit.
        while True:
            menu()

            # Get the user's menu selection.
            choice = input("Enter your choice: ").strip()

            if not choice:
                print("Field cannot be empty.")
                continue

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
                    print("Invalid input. Age must be a number.")
                    continue

                department = input("Department: ").strip()

                if not department:
                    print("Department cannot be empty.")
                    continue

                add_student(name, age, department)

            elif choice == "2":
                view_students()

            elif choice == "3":
                try:
                    student_id = int(input("Student ID: "))
                except ValueError:
                    print("Invalid input. Enter a valid Student ID")
                    continue

                department = input("New Department: ").strip()

                if not department:
                    print("Department cannot be empty.")
                    continue

                update_student(student_id, department)

            elif choice == "4":
                try:
                    student_id = int(input("Student ID: "))
                except ValueError:
                    print("Invalid Student ID.")
                    continue

                delete_student(student_id)

            elif choice == "5":
                view_logs()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Please, choose a valid option.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

if __name__ == "__main__":
    main()
    

            
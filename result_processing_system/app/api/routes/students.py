import sqlite3

from fastapi import APIRouter, HTTPException, status

from app.database.connection import create_connection

from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)

from app.services.student_service import (
    create_student,
    get_student_by_id,
    update_student,
    delete_student,
)

from app.core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
    ResourceNotFoundError,
)


# Create the students router.
# All student endpoints will begin with /students.
router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


# ============================================================
# CREATE STUDENT
# POST /students/
# ============================================================

@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_student(student: StudentCreate):
    """Create a new student."""

    try:
        # Send the student's data to the service layer.
        result = create_student(
            student.student_number,
            student.name,
            student.email,
            student.department,
            student.level,
        )

        # Return the newly created student.
        return {
            "id": result[0],
            "student_number": result[1],
            "name": result[2],
            "email": result[3],
            "department": result[4],
            "level": result[5],
        }

    # Student number or email already exists.
    except DuplicateResourceError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    # Database connection or database operation failed.
    except DatabaseError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error


# ============================================================
# GET ALL STUDENTS
# GET /students/
# ============================================================

@router.get("/")
def get_students():
    """Return all students."""

    # Create a database connection.
    connection = create_connection()

    # Check whether the connection was successful.
    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to connect to database.",
        )

    try:
        # Create a database cursor.
        cursor = connection.cursor()

        # Retrieve all students.
        cursor.execute("""
            SELECT
                id,
                student_number,
                name,
                email,
                department,
                level,
                created_at,
                updated_at
            FROM students
            ORDER BY id
        """)

        students = cursor.fetchall()

        # Return students as dictionaries.
        return [
            {
                "id": student[0],
                "student_number": student[1],
                "name": student[2],
                "email": student[3],
                "department": student[4],
                "level": student[5],
                "created_at": student[6],
                "updated_at": student[7],
            }
            for student in students
        ]

    except sqlite3.Error as error:
        # Convert database errors into an HTTP 500 response.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve students.",
        ) from error

    finally:
        # Always close the database connection.
        connection.close()


# ============================================================
# GET ONE STUDENT
# GET /students/{student_id}
# ============================================================

@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_student(student_id: int):
    """Return one student by ID."""

    try:
        # Get the student from the service layer.
        result = get_student_by_id(student_id)

        # Return the student.
        return {
            "id": result[0],
            "student_number": result[1],
            "name": result[2],
            "email": result[3],
            "department": result[4],
            "level": result[5],
        }

    # Student does not exist.
    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    # Database error.
    except DatabaseError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error


# ============================================================
# UPDATE STUDENT
# PUT /students/{student_id}
# ============================================================

@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update_existing_student(
    student_id: int,
    student: StudentUpdate,
):
    """Update an existing student."""

    try:
        # Send the updated data to the service layer.
        result = update_student(
            student_id,
            student.student_number,
            student.name,
            student.email,
            student.department,
            student.level,
        )

        # Return the updated student.
        return {
            "id": result[0],
            "student_number": result[1],
            "name": result[2],
            "email": result[3],
            "department": result[4],
            "level": result[5],
        }

    # Student does not exist.
    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    # Student number or email already exists.
    except DuplicateResourceError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    # Database error.
    except DatabaseError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error


# ============================================================
# DELETE STUDENT
# DELETE /students/{student_id}
# ============================================================

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_student(student_id: int):
    """Delete an existing student."""

    try:
        # Delete the student through the service layer.
        delete_student(student_id)

        # HTTP 204 means successful deletion with no response body.
        return None

    # Student does not exist.
    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    # Database error.
    except DatabaseError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error
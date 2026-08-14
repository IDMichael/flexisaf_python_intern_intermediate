import sqlite3

from fastapi import APIRouter, HTTPException, status

from app.database.connection import create_connection

from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
)

from app.services.course_service import (
    create_course,
    get_course_by_id,
    update_course,
    delete_course,
    )


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_course(course: CourseCreate):
    """Create a new course."""

    try:
        result = create_course(
            course.course_code,
            course.course_name,
            course.credit_unit
        )

        return {
            "id": result[0],
            "course_code": result[1],
            "course_name": result[2],
            "credit_unit": result[3],
        }

    except sqlite3.IntegrityError as error:
        raise HTTPException(
            status_code=409,
            detail="Course code already exists."
        ) from error


@router.get("/")
def get_courses():
    """Return all courses."""

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Unable to connect to database."
        )

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                course_name,
                course_code,
                credit_unit,
                created_at,
                updated_at
            FROM courses
            ORDER BY id
        """)

        courses = cursor.fetchall()

        return [
            {
                "id": course[0],
                "course_name": course[1],
                "course_code": course[2],
                "credit_unit": course[3],
                "created_at": course[4],
                "updated_at": course[5],
            }
            for course in courses
        ]

    finally:
        connection.close()

@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def get_course(course_id: int):
    """Return a single course by ID."""

    course = get_course_by_id(course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    return {
        "id": course[0],
        "course_code": course[1],
        "course_name": course[2],
        "credit_unit": course[3],
    }

@router.put(
    "/{course_id}",
    response_model=CourseResponse
)
def update_existing_course(
    course_id: int,
    course: CourseUpdate
):
    """Update an existing course."""

    try:
        result = update_course(
            course_id,
            course.course_code,
            course.course_name,
            course.credit_unit
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found."
            )
        
        return {
            "id": result[0],
            "course_code": result[1],
            "course_name": result[2],
            "credit_unit": result[3],
        }

    except sqlite3.IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course code already exists."
        ) from error

@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_course(course_id: int):
    """Delete an existing course."""

    deleted = delete_course(course_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    return None
        
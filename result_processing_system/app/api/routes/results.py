from fastapi import APIRouter, status, HTTPException

from app.database.connection import create_connection

from app.schemas.result import (
    ResultCreate,
    ResultResponse,
    ResultUpdate,
)

from app.services.result_database_service import (
    create_result,
    get_result_by_id,
    update_result,
    delete_result
)


router = APIRouter(
    prefix="/results",
    tags=["Results"],
)


@router.post(
    "/",
    response_model=ResultResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_result(result: ResultCreate):
    """Create a student result."""

    data = create_result(
        result.student_id,
        result.course_id,
        result.score,
        result.semester,
        result.session,
    )

    return {
        "id": data[0],
        "student_id": data[1],
        "course_id": data[2],
        "score": data[3],
        "semester": data[4],
        "session": data[5],
    }


@router.get("/")
def get_results():
    """Return all student results."""

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Unable to connect to database.",
        )

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                results.id,
                results.student_id,
                students.name,
                results.course_id,
                courses.course_name,
                courses.course_code,
                results.score,
                results.semester,
                results.session,
                courses.credit_unit,
                results.created_at,
                results.updated_at
            FROM results
            JOIN students
                ON results.student_id = students.id
            JOIN courses
                ON results.course_id = courses.id
            ORDER BY results.id
        """)

        results = cursor.fetchall()

        return [
            {
                "id": result[0],
                "student_id": result[1],
                "student_name": result[2],
                "course_id": result[3],
                "course_name": result[4],
                "course_code": result[5],
                "score": result[6],
                "semester": result[7],
                "session": result[8],
                "credit_unit": result[9],
                "created_at": result[10],
                "updated_at": result[11],
            }
            for result in results
        ]

    finally:
        connection.close()

@router.get(
    "/{result_id}",
    response_model=ResultResponse,
)
def get_result(result_id: int):
    """Return a single student result."""

    data = get_result_by_id(result_id)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found.",
        )

    return {
        "id": data[0],
        "student_id": data[1],
        "course_id": data[2],
        "score": data[3],
        "semester": data[4],
        "session": data[5],
    }


@router.put(
    "/{result_id}",
    response_model=ResultResponse,
)
def update_existing_result(
    result_id: int,
    result: ResultUpdate,
):
    """Update an existing student result."""

    data = update_result(
        result_id,
        result.student_id,
        result.course_id,
        result.score,
        result.semester,
        result.session,
    )

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found.",
        )

    return {
        "id": data[0],
        "student_id": data[1],
        "course_id": data[2],
        "score": data[3],
        "semester": data[4],
        "session": data[5],
    }

@router.delete(
    "/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_result(result_id: int):
    """Delete an existing student result."""

    deleted = delete_result(result_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found.",
        )

    return None
from fastapi import APIRouter, HTTPException

from app.analytics.performance import PerformanceAnalytics
from app.api.routes.analytics import get_all_results


router = APIRouter(
    prefix="/academic",
    tags=["Academic Performance"],
)


@router.get("/students/{student_id}/cgpa")
def get_student_cgpa(student_id: int):
    """Return a student's cumulative GPA."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    try:
        cgpa = analytics.calculate_cgpa(
            student_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return {
        "student_id": student_id,
        "cgpa": cgpa,
    }

@router.get(
    "/students/{student_id}/gpa"
)
def get_student_gpa(
    student_id: int,
    semester: str,
    session: str,
):
    """Return GPA for a specific semester."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    try:
        gpa = analytics.calculate_semester_gpa(
            student_id,
            semester,
            session,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return {
        "student_id": student_id,
        "semester": semester,
        "session": session,
        "gpa": gpa,
    }

@router.get(
    "/students/{student_id}/history"
)
def get_academic_history(
    student_id: int,
):
    """Return semester-by-semester history."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    try:
        history = analytics.academic_history(
            student_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return {
        "student_id": student_id,
        "history": history,
    }
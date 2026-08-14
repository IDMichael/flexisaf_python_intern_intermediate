from fastapi import APIRouter, HTTPException

from app.analytics.performance import PerformanceAnalytics
from app.database.connection import create_connection


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


def get_all_results():
    """
    Retrieve all result data required by the analytics engine.
    """

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Unable to connect to database.",
        )

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                r.student_id,
                s.name AS student_name,
                r.course_id,
                c.course_code,
                r.score,
                c.credit_unit
            FROM results r
            INNER JOIN students s
                ON r.student_id = s.id
            INNER JOIN courses c
                ON r.course_id = c.id
            ORDER BY r.student_id, c.course_code
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "student_id": row[0],
                "student_name": row[1],
                "course_id": row[2],
                "course_code": row[3],
                "score": row[4],
                "credit_unit": row[5],
            }
            for row in rows
        ]

    finally:
        connection.close()


@router.get("/students")
def student_statistics():
    """Return GPA and performance statistics for every student."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    statistics = analytics.calculate_student_statistics()

    return statistics.to_dict(
        orient="records"
    )


@router.get("/ranking")
def student_ranking():
    """Return students ranked by GPA."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    ranking = analytics.rank_students()

    return ranking.to_dict(
        orient="records"
    )


@router.get("/class")
def class_statistics():
    """Return overall class performance."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    return {
        "class_average": analytics.class_average(),
        "pass_rate": analytics.pass_rate(),
        "failure_rate": analytics.failure_rate(),
    }


@router.get("/courses")
def course_statistics():
    """Return performance statistics for every course."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    statistics = analytics.course_statistics()

    return statistics.to_dict(
        orient="records"
    )


@router.get("/summary")
def performance_summary():
    """Return a complete performance summary."""

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = PerformanceAnalytics(results)

    ranking = analytics.rank_students()

    return {
        "class_average": analytics.class_average(),
        "pass_rate": analytics.pass_rate(),
        "failure_rate": analytics.failure_rate(),
        "student_count": len(
            ranking
        ),
        "top_student": (
            ranking.iloc[0].to_dict()
            if not ranking.empty
            else None
        ),
        "course_statistics": (
            analytics
            .course_statistics()
            .to_dict(orient="records")
        ),
    }
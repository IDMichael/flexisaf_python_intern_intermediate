from fastapi import (APIRouter, Depends, HTTPException,)
from app.api.dependencies import(get_current_user,)
from app.analytics.advanced import (
    AdvancedPerformanceAnalytics,
)
from app.api.routes.analytics import (
    get_all_results,
)

router = APIRouter(
    prefix="/advanced-analytics",
    tags=["Advanced Analytics"],
)

def get_analytics():
    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    return AdvancedPerformanceAnalytics(
        results
    )

@router.get("/grades")
def grade_distribution(
    current_user=Depends(get_current_user),
    ):
    analytics = get_analytics()

    return {
        "distribution":
        analytics.grade_distribution()
    }

@router.get("/courses")
def course_performance():
    analytics = get_analytics()

    data = analytics.course_performance()

    return data.to_dict(
        orient="records"
    )

@router.get("/courses/weakest")
def weakest_courses(
    limit: int = 5,
):
    if limit <= 0:
        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than zero.",
        )

    analytics = get_analytics()

    data = analytics.weakest_courses(
        limit=limit
    )

    return data.to_dict(
        orient="records"
    )


@router.get("/courses/strongest")
def strongest_courses(
    limit: int = 5,
):
    if limit <= 0:
        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than zero.",
        )

    analytics = get_analytics()

    data = analytics.strongest_courses(
        limit=limit
    )

    return data.to_dict(
        orient="records"
    )


@router.get(
    "/students/{student_id}"
)
def student_performance(
    student_id: int,
):
    analytics = get_analytics()

    try:
        return analytics.student_performance(
            student_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error


@router.get("/at-risk")
def at_risk_students(
    threshold: float = 2.0,
):
    if threshold < 0:
        raise HTTPException(
            status_code=400,
            detail=(
                "Threshold cannot be negative."
            ),
        )

    analytics = get_analytics()

    return analytics.at_risk_students(
        threshold=threshold
    )


@router.get(
    "/students/{student_id}/trend"
)
def student_trend(
    student_id: int,
):
    analytics = get_analytics()

    try:
        return analytics.performance_trend(
            student_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
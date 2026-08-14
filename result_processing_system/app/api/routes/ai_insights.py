from fastapi import APIRouter, HTTPException

from app.analytics.advanced import (
    AdvancedPerformanceAnalytics,
)

from app.api.routes.analytics import (
    get_all_results,
)

from app.services.ai_insight_service import (
    AIInsightService,
)


router = APIRouter(
    prefix="/ai-insights",
    tags=["AI Insights"],
)


@router.get(
    "/students/{student_id}"
)
def generate_student_insight(
    student_id: int,
):
    """
    Generate a performance explanation
    for one student.
    """

    results = get_all_results()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No result data available.",
        )

    analytics = AdvancedPerformanceAnalytics(
        results
    )

    try:
        student_analysis = (
            analytics.student_performance(
                student_id
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    ai_service = AIInsightService()

    return ai_service.generate_insight(
        student_analysis
    )
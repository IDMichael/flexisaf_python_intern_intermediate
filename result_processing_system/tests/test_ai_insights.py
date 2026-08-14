from app.services.ai_insight_service import (
    AIInsightService,
)


def sample_analysis():
    return {
        "student_id": 1,
        "student_name": "John Doe",
        "average_score": 47.5,
        "highest_score": 72,
        "lowest_score": 25,
        "strongest_course": "CSC301",
        "weakest_course": "MAT301",
        "gpa": 1.82,
    }


def test_ai_insight():

    service = AIInsightService()

    result = service.generate_insight(
        sample_analysis()
    )

    assert result["student_id"] == 1

    assert result["student_name"] == (
        "John Doe"
    )

    assert result["cgpa"] == 1.82

    assert "MAT301" in (
        result["insight"]
    )

    assert len(
        result["reasons"]
    ) > 0


def test_recommendations():

    service = AIInsightService()

    recommendations = (
        service.generate_recommendations(
            sample_analysis()
        )
    )

    assert len(recommendations) > 0


def test_good_student():

    service = AIInsightService()

    analysis = {
        "student_id": 2,
        "student_name": "Jane Doe",
        "average_score": 82,
        "highest_score": 95,
        "lowest_score": 70,
        "strongest_course": "CSC301",
        "weakest_course": "ENG301",
        "gpa": 4.8,
    }

    result = service.generate_insight(
        analysis
    )

    assert result["cgpa"] == 4.8

    assert (
        "No major academic warning"
        in result["insight"]
    )
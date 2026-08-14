from app.analytics.advanced import (
    AdvancedPerformanceAnalytics,
)


def sample_results():
    return [
        {
            "student_id": 1,
            "student_name": "John",
            "course_code": "CSC301",
            "score": 80,
            "credit_unit": 3,
            "semester": "First",
            "session": "2025/2026",
        },
        {
            "student_id": 1,
            "student_name": "John",
            "course_code": "MAT301",
            "score": 60,
            "credit_unit": 3,
            "semester": "First",
            "session": "2025/2026",
        },
        {
            "student_id": 2,
            "student_name": "Jane",
            "course_code": "CSC301",
            "score": 35,
            "credit_unit": 3,
            "semester": "First",
            "session": "2025/2026",
        },
    ]


def test_grade_distribution():
    analytics = AdvancedPerformanceAnalytics(
        sample_results()
    )

    distribution = (
        analytics.grade_distribution()
    )

    assert distribution["A"] == 1
    assert distribution["B"] == 1
    assert distribution["F"] == 1


def test_course_performance():
    analytics = AdvancedPerformanceAnalytics(
        sample_results()
    )

    data = analytics.course_performance()

    csc = data[
        data["course_code"] == "CSC301"
    ].iloc[0]

    assert csc["average_score"] == 57.5
    assert csc["pass_rate"] == 50.0
    assert csc["failure_rate"] == 50.0


def test_student_performance():
    analytics = AdvancedPerformanceAnalytics(
        sample_results()
    )

    result = analytics.student_performance(1)

    assert result["student_name"] == "John"
    assert result["highest_score"] == 80
    assert result["lowest_score"] == 60


def test_at_risk_students():
    analytics = AdvancedPerformanceAnalytics(
        sample_results()
    )

    students = analytics.at_risk_students(
        threshold=2.0
    )

    assert len(students) >= 1


def test_student_without_results():
    analytics = AdvancedPerformanceAnalytics(
        sample_results()
    )

    try:
        analytics.student_performance(999)

        assert False

    except ValueError as error:
        assert "no results" in str(error).lower()
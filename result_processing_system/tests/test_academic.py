from app.analytics.performance import (
    PerformanceAnalytics,
)


def test_semester_gpa():

    results = [
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
    ]

    analytics = PerformanceAnalytics(results)

    gpa = analytics.calculate_semester_gpa(
        1,
        "First",
        "2025/2026",
    )

    assert gpa == 4.5
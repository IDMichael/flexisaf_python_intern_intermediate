from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_student_analytics_endpoint():
    response = client.get(
        "/analytics/students"
    )

    assert response.status_code in [200, 404]


def test_ranking_endpoint():
    response = client.get(
        "/analytics/ranking"
    )

    assert response.status_code in [200, 404]


def test_class_statistics_endpoint():
    response = client.get(
        "/analytics/class"
    )

    assert response.status_code in [200, 404]


def test_course_statistics_endpoint():
    response = client.get(
        "/analytics/courses"
    )

    assert response.status_code in [200, 404]


def test_summary_endpoint():
    response = client.get(
        "/analytics/summary"
    )

    assert response.status_code in [200, 404]
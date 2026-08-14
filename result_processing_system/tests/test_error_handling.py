from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_score_returns_422():
    response = client.post(
        "/results/",
        json={
            "student_id": 1,
            "course_id": 1,
            "score": 101,
            "semester": "First",
            "session": "2025/2026",
        },
    )

    assert response.status_code == 422


def test_negative_score_returns_422():
    response = client.post(
        "/results/",
        json={
            "student_id": 1,
            "course_id": 1,
            "score": -5,
            "semester": "First",
            "session": "2025/2026",
        },
    )

    assert response.status_code == 422


def test_nonexistent_student_returns_404():
    response = client.post(
        "/results/",
        json={
            "student_id": 999999,
            "course_id": 1,
            "score": 80,
            "semester": "First",
            "session": "2025/2026",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["code"] == "RESOURCE_NOT_FOUND"
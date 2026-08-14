from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Result Processing System API is running."
    }


def test_create_student():
    response = client.post(
        "/students/",
        json={
            "student_number": "API-STU-001",
            "name": "API Student",
            "email": "api.student@example.com",
            "department": "Computer Science",
            "level": 300
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["student_number"] == "API-STU-001"
    assert data["name"] == "API Student"


def test_create_course():
    response = client.post(
        "/courses/",
        json={
            "course_code": "API-CSC-301",
            "course_name": "API Database Systems",
            "credit_unit": 3
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["course_code"] == "API-CSC-301"
    assert data["credit_unit"] == 3


def test_invalid_score_is_rejected():
    response = client.post(
        "/results/",
        json={
            "student_id": 1,
            "course_id": 1,
            "score": 101,
            "semester": "First",
            "session": "2025/2026"
        }
    )

    assert response.status_code == 422


def test_negative_score_is_rejected():
    response = client.post(
        "/results/",
        json={
            "student_id": 1,
            "course_id": 1,
            "score": -1,
            "semester": "First",
            "session": "2025/2026"
        }
    )

    assert response.status_code == 422


# ============================================================
# STUDENT UPDATE
# ============================================================

def test_update_student():
    create_response = client.post(
        "/students/",
        json={
            "student_number": "UPDATE-STU-001",
            "name": "Original Student",
            "email": "original.student@example.com",
            "department": "Computer Science",
            "level": 200
        }
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    update_response = client.put(
        f"/students/{student_id}",
        json={
            "student_number": "UPDATE-STU-001",
            "name": "Updated Student",
            "email": "updated.student@example.com",
            "department": "Software Engineering",
            "level": 300
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == student_id
    assert data["name"] == "Updated Student"
    assert data["email"] == "updated.student@example.com"
    assert data["department"] == "Software Engineering"
    assert data["level"] == 300


def test_update_nonexistent_student():
    response = client.put(
        "/students/999999",
        json={
            "student_number": "NONEXISTENT-STU",
            "name": "Nobody",
            "email": "nobody@example.com",
            "department": "Computer Science",
            "level": 300
        }
    )

    assert response.status_code == 404


# ============================================================
# STUDENT DELETE
# ============================================================

def test_delete_student():
    create_response = client.post(
        "/students/",
        json={
            "student_number": "DELETE-STU-001",
            "name": "Delete Student",
            "email": "delete.student@example.com",
            "department": "Computer Science",
            "level": 200
        }
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/students/{student_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/students/{student_id}"
    )

    assert get_response.status_code == 404


def test_delete_nonexistent_student():
    response = client.delete(
        "/students/999999"
    )

    assert response.status_code == 404


# ============================================================
# COURSE UPDATE
# ============================================================

def test_update_course():
    create_response = client.post(
        "/courses/",
        json={
            "course_code": "UPDATE-CSC-001",
            "course_name": "Original Course",
            "credit_unit": 2
        }
    )

    assert create_response.status_code == 201

    course_id = create_response.json()["id"]

    update_response = client.put(
        f"/courses/{course_id}",
        json={
            "course_code": "UPDATE-CSC-001",
            "course_name": "Updated Course",
            "credit_unit": 3
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == course_id
    assert data["course_code"] == "UPDATE-CSC-001"
    assert data["course_name"] == "Updated Course"
    assert data["credit_unit"] == 3


def test_update_nonexistent_course():
    response = client.put(
        "/courses/999999",
        json={
            "course_code": "NONEXISTENT-CSC",
            "course_name": "Nobody Course",
            "credit_unit": 3
        }
    )

    assert response.status_code == 404


# ============================================================
# COURSE DELETE
# ============================================================

def test_delete_course():
    create_response = client.post(
        "/courses/",
        json={
            "course_code": "DELETE-CSC-001",
            "course_name": "Delete Course",
            "credit_unit": 3
        }
    )

    assert create_response.status_code == 201

    course_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/courses/{course_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/courses/{course_id}"
    )

    assert get_response.status_code == 404


def test_delete_nonexistent_course():
    response = client.delete(
        "/courses/999999"
    )

    assert response.status_code == 404


# ============================================================
# RESULT UPDATE
# ============================================================

def test_update_result():
    student_response = client.post(
        "/students/",
        json={
            "student_number": "RESULT-UPDATE-STU",
            "name": "Result Update Student",
            "email": "result.update.student@example.com",
            "department": "Computer Science",
            "level": 300
        }
    )

    assert student_response.status_code == 201

    student_id = student_response.json()["id"]

    course_response = client.post(
        "/courses/",
        json={
            "course_code": "RESULT-UPDATE-CSC",
            "course_name": "Result Update Course",
            "credit_unit": 3
        }
    )

    assert course_response.status_code == 201

    course_id = course_response.json()["id"]

    result_response = client.post(
        "/results/",
        json={
            "student_id": student_id,
            "course_id": course_id,
            "score": 60,
            "semester": "First",
            "session": "2025/2026"
        }
    )

    assert result_response.status_code == 201

    result_id = result_response.json()["id"]

    update_response = client.put(
        f"/results/{result_id}",
        json={
            "student_id": student_id,
            "course_id": course_id,
            "score": 85,
            "semester": "Second",
            "session": "2025/2026"
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == result_id
    assert data["student_id"] == student_id
    assert data["course_id"] == course_id
    assert data["score"] == 85
    assert data["semester"] == "Second"
    assert data["session"] == "2025/2026"


def test_update_nonexistent_result():
    response = client.put(
        "/results/999999",
        json={
            "student_id": 1,
            "course_id": 1,
            "score": 85,
            "semester": "Second",
            "session": "2025/2026"
        }
    )

    assert response.status_code == 404


# ============================================================
# RESULT DELETE
# ============================================================

def test_delete_result():
    student_response = client.post(
        "/students/",
        json={
            "student_number": "RESULT-DELETE-STU",
            "name": "Result Delete Student",
            "email": "result.delete.student@example.com",
            "department": "Computer Science",
            "level": 300
        }
    )

    assert student_response.status_code == 201

    student_id = student_response.json()["id"]

    course_response = client.post(
        "/courses/",
        json={
            "course_code": "RESULT-DELETE-CSC",
            "course_name": "Result Delete Course",
            "credit_unit": 3
        }
    )

    assert course_response.status_code == 201

    course_id = course_response.json()["id"]

    result_response = client.post(
        "/results/",
        json={
            "student_id": student_id,
            "course_id": course_id,
            "score": 75,
            "semester": "First",
            "session": "2025/2026"
        }
    )

    assert result_response.status_code == 201

    result_id = result_response.json()["id"]

    delete_response = client.delete(
        f"/results/{result_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/results/{result_id}"
    )

    assert get_response.status_code == 404


def test_delete_nonexistent_result():
    response = client.delete(
        "/results/999999"
    )

    assert response.status_code == 404
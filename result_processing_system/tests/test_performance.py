import pytest

from app.analytics.performance import PerformanceAnalytics


@pytest.fixture
def results():
    return [
        {
            "student_id": 1,
            "student_name": "John Doe",
            "course_code": "CSC301",
            "score": 80,
            "credit_unit": 3,
        },
        {
            "student_id": 1,
            "student_name": "John Doe",
            "course_code": "MAT301",
            "score": 70,
            "credit_unit": 3,
        },
        {
            "student_id": 2,
            "student_name": "Jane Doe",
            "course_code": "CSC301",
            "score": 60,
            "credit_unit": 3,
        },
        {
            "student_id": 2,
            "student_name": "Jane Doe",
            "course_code": "MAT301",
            "score": 50,
            "credit_unit": 3,
        },
    ]


def test_student_statistics(results):
    analytics = PerformanceAnalytics(results)

    statistics = analytics.calculate_student_statistics()

    john = statistics[
        statistics["student_id"] == 1
    ].iloc[0]

    jane = statistics[
        statistics["student_id"] == 2
    ].iloc[0]

    assert john["gpa"] == 5.00
    assert jane["gpa"] == 3.50


def test_student_ranking(results):
    analytics = PerformanceAnalytics(results)

    ranking = analytics.rank_students()

    assert ranking.iloc[0]["student_name"] == "John Doe"
    assert ranking.iloc[0]["rank"] == 1

    assert ranking.iloc[1]["student_name"] == "Jane Doe"
    assert ranking.iloc[1]["rank"] == 2


def test_class_average(results):
    analytics = PerformanceAnalytics(results)

    assert analytics.class_average() == 65.00


def test_pass_rate(results):
    analytics = PerformanceAnalytics(results)

    assert analytics.pass_rate() == 100.00


def test_failure_rate(results):
    analytics = PerformanceAnalytics(results)

    assert analytics.failure_rate() == 0.00


def test_course_statistics(results):
    analytics = PerformanceAnalytics(results)

    statistics = analytics.course_statistics()

    csc = statistics[
        statistics["course_code"] == "CSC301"
    ].iloc[0]

    assert csc["average_score"] == 70.00
    assert csc["highest_score"] == 80
    assert csc["lowest_score"] == 60
    assert csc["number_of_students"] == 2


def test_empty_results_are_rejected():
    analytics = PerformanceAnalytics([])

    with pytest.raises(ValueError):
        analytics.calculate_student_statistics()


def test_missing_required_column_is_rejected():
    results = [
        {
            "student_id": 1,
            "student_name": "John Doe",
            "score": 80,
        }
    ]

    analytics = PerformanceAnalytics(results)

    with pytest.raises(ValueError):
        analytics.calculate_student_statistics()


def test_score_above_100_is_rejected(results):
    results[0]["score"] = 101

    analytics = PerformanceAnalytics(results)

    with pytest.raises(ValueError):
        analytics.calculate_student_statistics()


def test_negative_score_is_rejected(results):
    results[0]["score"] = -1

    analytics = PerformanceAnalytics(results)

    with pytest.raises(ValueError):
        analytics.calculate_student_statistics()


def test_missing_score_is_rejected(results):
    results[0]["score"] = None

    analytics = PerformanceAnalytics(results)

    with pytest.raises(ValueError):
        analytics.calculate_student_statistics()


def test_missing_credit_unit_is_rejected(results):
    results[0]["credit_unit"] = None

    analytics = PerformanceAnalytics(results)

    with pytest.raises(ValueError):
        analytics.calculate_student_statistics()


def test_invalid_credit_unit_is_rejected(results):
    results[0]["credit_unit"] = 0

    analytics = PerformanceAnalytics(results)

    with pytest.raises(ValueError):
        analytics.calculate_student_statistics()


def test_tied_students_receive_same_rank():
    results = [
        {
            "student_id": 1,
            "student_name": "John Doe",
            "course_code": "CSC301",
            "score": 80,
            "credit_unit": 3,
        },
        {
            "student_id": 2,
            "student_name": "Jane Doe",
            "course_code": "CSC301",
            "score": 80,
            "credit_unit": 3,
        },
        {
            "student_id": 3,
            "student_name": "Mark Doe",
            "course_code": "CSC301",
            "score": 60,
            "credit_unit": 3,
        },
    ]

    analytics = PerformanceAnalytics(results)

    ranking = analytics.rank_students()

    assert ranking.iloc[0]["rank"] == 1
    assert ranking.iloc[1]["rank"] == 1
    assert ranking.iloc[2]["rank"] == 3
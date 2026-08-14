import pytest

from app.services.result_service import (
    InvalidCreditUnitError,
    InvalidScoreError,
    NoResultError,
    calculate_grade,
    calculate_gpa,
    calculate_quality_point,
    validate_credit_unit,
    validate_score,
)


# -------------------------
# Score validation
# -------------------------

def test_valid_score():
    assert validate_score(75) == 75.0


@pytest.mark.parametrize("score", [0, 40, 50, 70, 100])
def test_boundary_scores_are_valid(score):
    assert validate_score(score) == float(score)


@pytest.mark.parametrize(
    "score",
    [-1, -100, 101, 150]
)
def test_invalid_score_range(score):
    with pytest.raises(InvalidScoreError):
        validate_score(score)


@pytest.mark.parametrize(
    "score",
    [None, "80", [], {}, True, False]
)
def test_invalid_score_type(score):
    with pytest.raises(InvalidScoreError):
        validate_score(score)


# -------------------------
# Grade calculation
# -------------------------

@pytest.mark.parametrize(
    "score, expected_grade, expected_point",
    [
        (100, "A", 5.0),
        (70, "A", 5.0),
        (69, "B", 4.0),
        (60, "B", 4.0),
        (59, "C", 3.0),
        (50, "C", 3.0),
        (49, "D", 2.0),
        (45, "D", 2.0),
        (44, "E", 1.0),
        (40, "E", 1.0),
        (39, "F", 0.0),
        (0, "F", 0.0),
    ]
)
def test_grade_boundaries(
    score,
    expected_grade,
    expected_point
):
    grade, point = calculate_grade(score)

    assert grade == expected_grade
    assert point == expected_point


# -------------------------
# Credit-unit validation
# -------------------------

@pytest.mark.parametrize(
    "credit_unit",
    [1, 2, 3, 4, 5, 6]
)
def test_valid_credit_units(credit_unit):
    assert validate_credit_unit(credit_unit) == credit_unit


@pytest.mark.parametrize(
    "credit_unit",
    [0, -1, -5]
)
def test_invalid_credit_units(credit_unit):
    with pytest.raises(InvalidCreditUnitError):
        validate_credit_unit(credit_unit)


@pytest.mark.parametrize(
    "credit_unit",
    [3.5, "3", None, [], True, False]
)
def test_invalid_credit_unit_types(credit_unit):
    with pytest.raises(InvalidCreditUnitError):
        validate_credit_unit(credit_unit)


# -------------------------
# Quality points
# -------------------------

def test_quality_point():
    assert calculate_quality_point(80, 3) == 15.0


def test_failed_course_quality_point():
    assert calculate_quality_point(30, 3) == 0.0


# -------------------------
# GPA
# -------------------------

def test_gpa():
    results = [
        {
            "score": 80,
            "credit_unit": 3
        },
        {
            "score": 65,
            "credit_unit": 3
        },
        {
            "score": 55,
            "credit_unit": 2
        }
    ]

    assert calculate_gpa(results) == 4.13


def test_gpa_with_different_credit_units():
    results = [
        {
            "score": 70,
            "credit_unit": 4
        },
        {
            "score": 60,
            "credit_unit": 2
        }
    ]

    # 5 × 4 = 20
    # 4 × 2 = 8
    # GPA = 28 / 6 = 4.67

    assert calculate_gpa(results) == 4.67


def test_gpa_with_all_failed_courses():
    results = [
        {
            "score": 20,
            "credit_unit": 3
        },
        {
            "score": 35,
            "credit_unit": 2
        }
    ]

    assert calculate_gpa(results) == 0.0


def test_gpa_without_results():
    with pytest.raises(NoResultError):
        calculate_gpa([])


def test_gpa_with_invalid_score():
    results = [
        {
            "score": 120,
            "credit_unit": 3
        }
    ]

    with pytest.raises(InvalidScoreError):
        calculate_gpa(results)


def test_gpa_with_invalid_credit_unit():
    results = [
        {
            "score": 80,
            "credit_unit": 0
        }
    ]

    with pytest.raises(InvalidCreditUnitError):
        calculate_gpa(results)
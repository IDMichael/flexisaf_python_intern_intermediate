from decimal import Decimal, ROUND_HALF_UP

class ResultProcessingError(Exception):
    """Base exception for result-processing errors."""

class InvalidScoreError(ResultProcessingError):
    """Raised when a score is outsiode the valid range."""

class InvalidCreditUnitError(ResultProcessingError):
    """Raised when a credit unit is invalid."""

class NoResultError(ResultProcessingError):
    """Raised when GPA calculation receives no results."""

def validate_score(score):
    """Validate an examination score.
    Valid scores are between 0 and 100 inclusive.
    """
    if score is None:
        raise InvalidScoreError("Score is required.")

    if not isinstance(score, (int, float)):
        raise InvalidScoreError("Score must be a number.")

    if isinstance(score, bool):
        raise InvalidScoreError("Score must be a number.")

    if score < 0 or score > 100:
        raise InvalidScoreError("Score must be between 0 and 100.")

    return float(score)

def calculate_grade(score):
    """Return the grade and grade point for a score."""
    score = validate_score(score)

    if score >= 70:
        return "A", 5.0

    if score >= 60:
        return "B", 4.0

    if score >= 50:
        return "C", 3.0

    if score >= 45:
        return "D", 2.0

    if score >= 40:
        return "E", 1.0

    return "F", 0.0

def validate_credit_unit(credit_unit):
    """Validate a course credit unit."""

    if isinstance(credit_unit, bool):
        raise InvalidCreditUnitError("Credit unit must be a positive integer.")

    if not isinstance(credit_unit, int) or credit_unit <= 0:
        raise InvalidCreditUnitError("Credit unit must be greater than zero.")

    return credit_unit

def calculate_quality_point(score, credit_unit):
    """Calculate quality points.
    Quality Point = Grade Point x Credit Unit
    """ 

    credit_unit = validate_credit_unit(credit_unit)

    _, grade_point = calculate_grade(score)

    return grade_point * credit_unit

def calculate_gpa(results):
    """Calculate a student's GPA.
    Each result must contain:
    - score
    - credit_unit

    GPA = 
        ∑(Grade Point x Credit Unit)
        ----------------------------
                ∑(Credit Units)
    """
    if not results:
        raise NoResultError("Cannot calculate GPA without results.")

    total_quality_points = 0.0
    total_credit_units = 0

    for result in results:
        score = result["score"]
        credit_unit = result["credit_unit"]

        credit_unit = validate_credit_unit(credit_unit)

        quality_point = calculate_quality_point(score, credit_unit)

        total_quality_points += quality_point
        total_credit_units += credit_unit

    if total_credit_units <= 0:
        raise InvalidCreditUnitError("Total credit units must be greater than zero.")

    gpa = total_quality_points / total_credit_units

    return float(
        Decimal(str(gpa)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP
    ))

    
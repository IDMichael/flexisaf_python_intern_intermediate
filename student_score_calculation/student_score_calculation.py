# =========================================================
# GLOBAL SCOPE VARIABLE
# =========================================================
ACADEMY_NAME = "Imami Awesome Academy"

# =========================================================
# FUNCTION: STUDENT REPORT GENERATOR
# Requirements:
# - Uses *args for scores
# - Uses **kwargs for optional settings (weight, bonus)
# - Handles unpacked inputs from main code
# =========================================================
def generate_student_report(student_full_name, *exam_scores, **grading_options):

    # VALIDATE STUDENT NAME
    if not isinstance(student_full_name, str):
        raise TypeError("Student name must be a string.")

    if not student_full_name.strip():
        raise ValueError("Student name cannot be empty.")

    # VALIDATE SCORES EXIST
    if len(exam_scores) == 0:
        raise ValueError("At least one exam score is required.")

    # STRICT SCORE VALIDATION
    cleaned_scores = []

    for score in exam_scores:

        # Reject boolean (Python treats bool as int)
        if isinstance(score, bool):
            raise TypeError("Boolean values are not valid scores.")

        # Must be numeric
        if not isinstance(score, (int, float)):
            raise TypeError("All exam scores must be numbers.")

        # Reject NaN / Infinity
        if isinstance(score, float):
            if score != score or score in (float("inf"), float("-inf")):
                raise ValueError("Invalid score value (NaN or Infinity not allowed).")

        # Score range check
        if score < 0 or score > 100:
            raise ValueError("Scores must be between 0 and 100.")

        cleaned_scores.append(score)

    # COMPUTE TOTAL
    total_marks = sum(cleaned_scores)

    # EXTRACT GRADING SETTINGS (kwargs)
    weight = grading_options.get("weight", 1.0)
    bonus = grading_options.get("bonus", 0)

    # VALIDATE WEIGHT
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise TypeError("Weight must be a number.")

    if weight <= 0:
        raise ValueError("Weight must be greater than 0.")

    if isinstance(weight, float) and (weight != weight or weight in (float("inf"), float("-inf"))):
        raise ValueError("Invalid weight value.")

    # VALIDATE BONUS
    if isinstance(bonus, bool) or not isinstance(bonus, (int, float)):
        raise TypeError("Bonus must be a number.")

    if bonus < 0:
        raise ValueError("Bonus cannot be negative.")

    if isinstance(bonus, float) and (bonus != bonus or bonus in (float("inf"), float("-inf"))):
        raise ValueError("Invalid bonus value.")

    # CALCULATIONS
    weighted_marks = total_marks * weight
    final_marks = weighted_marks + bonus
    average_marks = final_marks / len(cleaned_scores)

    # GRADE CALCULATION
    if average_marks >= 90:
        grade = "A"
    elif average_marks >= 80:
        grade = "B"
    elif average_marks >= 70:
        grade = "C"
    elif average_marks >= 60:
        grade = "D"
    else:
        grade = "F"

    # REPORT OUTPUT
    report = {
        "academy": ACADEMY_NAME,
        "student": student_full_name,
        "scores": tuple(cleaned_scores),
        "total_marks": total_marks,
        "weight": weight,
        "bonus": bonus,
        "final_marks": final_marks,
        "average_marks": round(average_marks, 2),
        "grade": grade,
    }

    print("\n===== STUDENT PERFORMANCE REPORT =====")
    for key, value in report.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    return report

# MAIN PROGRAM (REQUIRED UNPACKING)
student_exam_scores = (75, 80, 92, 88)

grading_configuration = {
    "weight": 1.2,
    "bonus": 5
}

# SAFE EXECUTION BLOCK
try:
    generate_student_report(
        "Michael Ukana",
        *student_exam_scores,
        **grading_configuration
    )

except (ValueError, TypeError) as error:
    print(f"\nError: {error}")
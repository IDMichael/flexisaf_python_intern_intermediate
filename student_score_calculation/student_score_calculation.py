# Global configuration variable.
# This variable is outside the function, so it is in the global scope
# and can be accessed anywhere in the program.
ACADEMY_NAME = "Bright Future Academy"


# Function to generate and display a student's performance report.
# student_full_name      -> Normal positional parameter for the student's name.
# *exam_scores           -> Accepts multiple exam scores as a tuple.
# **grading_options      -> Accepts optional keyword settings as a dictionary.
def generate_student_report(student_full_name, *exam_scores, **grading_options):

    # Validate that at least one score was provided.
    # If no scores exist, raise an error to stop the program.
    if not exam_scores:
        raise ValueError("At least one exam score is required.")

    # Calculate the total score by summing all provided exam scores.
    total_marks = sum(exam_scores)

    # Retrieve the weight value from grading_options dictionary.
    # If weight is not provided, default value becomes 1.0.
    weight = grading_options.get("weight", 1.0)

    # Retrieve the bonus value from grading_options dictionary.
    # If bonus is not provided, default value becomes 0.
    bonus = grading_options.get("bonus", 0)

    # Apply the weight to the total marks.
    weighted_marks = total_marks * weight

    # Add bonus marks to the weighted marks.
    final_marks = weighted_marks + bonus

    # Calculate the average score after weighting and bonus adjustments.
    average_marks = final_marks / len(exam_scores)

    # Determine the student's grade based on the average score.
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

    # Store all generated report details inside a dictionary.
    report = {
        "academy": ACADEMY_NAME,
        "student": student_full_name,
        "scores": exam_scores,
        "total_marks": total_marks,
        "weight": weight,
        "bonus": bonus,
        "final_marks": final_marks,
        "average_marks": round(average_marks, 2),
        "grade": grade,
    }

    # Display report heading.
    print("\n===== STUDENT PERFORMANCE REPORT =====")

    # Loop through each key-value pair in the report dictionary
    # and display them in a readable format.
    for key, value in report.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    # Return the complete report dictionary.
    return report


# Tuple containing multiple student exam scores.
# This will later be unpacked into separate arguments using *.
student_exam_scores = (75, 80, 92, 88)


# Dictionary containing optional grading settings.
# This dictionary will later be unpacked using **.
grading_configuration = {
    "weight": 1.2,
    "bonus": 5
}


# Function call using unpacking.
# *student_exam_scores   -> Unpacks tuple values into separate score arguments.
# **grading_configuration -> Unpacks dictionary items into keyword arguments.
generate_student_report(
    "Michael Ukana",
    *student_exam_scores,
    **grading_configuration
)
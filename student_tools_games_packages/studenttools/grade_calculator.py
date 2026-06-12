"""
Grade calculation module.
Handles score validation, averaging, grading, and pass/fail logic.
"""
def validate_scores(scores):
	if not isinstance(scores, (list, tuple)):
		raise TypeError("Scores must be a list or tuple.")

	if len(scores) == 0:
		raise ValueError("Scores cannot be empty")

	for score in scores:
		if not isinstance(score, (int, float)):
			raise TypeError("All scores must be numbers.")

		if score < 0 or score > 100:
			raise ValueError("Scores must be between 0 and 100.")

def calculate_average(scores):
	validate_scores(scores)
	return sum(scores) / len(scores)


def get_letter_grade(average):
	if average >= 70:
		return "A"
	elif average >= 60:
		return "B"
	elif average >= 50:
		return "C"
	elif average >= 45:
		return "D"
	return "F"

def get_status(average):
	return "PASS" if average >= 50 else "FAIL"
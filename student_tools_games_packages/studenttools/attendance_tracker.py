"""
Attendance calculation module.
Calculate attendance percentage and status.
"""
def calculate_attendance(attended, total):
	if not isinstance(attended, int) or not isinstance(total, int):
		raise TypeError("Attendance values must be integers.")

	if attended < 0 or total < 0:
		raise ValueError("Attendance cannot be negative.")

	if total == 0:
		raise ValueError("Total classes must be greater than zero.")

	if attended > total:
		raise ValueError("Attended cannot exceed total classes.")

	return (attended / total) * 100

def get_attendance_status(attendance):
	if not isinstance(attendance, (int, float)):
		raise TypeError("Attendance must be a number.")
		
	if attendance >= 75:
		return "Good Standing"

	elif attendance >= 50:
		return "Warning"

	return "Poor Attendance"
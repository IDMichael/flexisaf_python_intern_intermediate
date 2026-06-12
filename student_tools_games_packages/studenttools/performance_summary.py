"""
Performance summary module.
Combines academic and attendance results intoa a report.
"""

def get_remark(grade, attendance_percentage):
	if grade == "A" and attendance_percentage >= 80:
		return "Outstanding Performance"

	if grade in ["B", "C"] and attendance_percentage >= 75:
		return "Good Performance"

	if grade in ["D", "F"]:
		return "Needs Academic improvement"

	return "Average Performance"


def generate_report(name, average, grade, status, attendance, attendance_status, remark):

	if not name:
		raise ValueError("Name cannot be empty.")
	return {
		"Name": name,
		"Average": round(average, 2),
		"Grade": grade,
		"Status": status,
		"Attendance": f"{attendance:.2f}%",
		"Attendance Status": attendance_status,
		"Remark": remark
		}

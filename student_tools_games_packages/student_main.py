from studenttools.grade_calculator import (
	calculate_average,
	get_letter_grade,
	get_status
	)

from studenttools.attendance_tracker import (
	calculate_attendance,
	get_attendance_status
	)

from studenttools.performance_summary import (
	get_remark,
	generate_report
	)

# ==== SAFE INPUT HELPERS ====
def get_string(prompt):
	while True:
		try:
			value = input(prompt).strip()
			if not value:
				print("Name cannot be empty.")
				continue
			return value
		except KeyboardInterrupt:
			print("Program stopped.")
			exit()

def get_int(prompt):
	while True:
		try:
			return int(input(prompt))
		except ValueError:
			print("Please enter a valid integer.")
		except KeyboardInterrupt:
			print("Program stopped.")
			exit()

def get_float(prompt):
	while True:
		try:
			return float(input(prompt))
		except ValueError:
			print("Please enter a valid number.")
		except KeyboardInterrupt:
			print("Program stopped.")
			exit()

# ==== MAIN PROGRAM ====
def main():
	try:
		name = get_string("Enter student name: ")

		if not name:
			raise ValueError("Name cannot be empty.")

		# ==== SCORES ====
		num = get_int("How many subjects? ")

		if num <= 0:
			raise ValueError("Number of subjects must be greater than 0.")

		scores = []
		for i in range(num):
			while True:
				score = get_float(f"Enter score {i + 1}: ")

				if 0 <= score <= 100:
					scores.append(score)
					break
				print("Score must be between 0 and 100.")

		average = calculate_average(scores)
		grade = get_letter_grade(average)
		status = get_status(average)

		# ==== ATTENDANCE ====
		attended = get_int("Classes attended: ")
		total = get_int("Total classes: ")

		attendance_percentage = calculate_attendance(attended, total)
		attendance_status = get_attendance_status(attendance_percentage)

		# ==== REMARK ====
		remark = get_remark(grade, attendance_percentage)

		# ==== REPORT ====
		report = generate_report(
			name, average, grade, status, attendance_percentage, attendance_status, remark)

		# ==== OUTPUT ====
		print("\n" + "=" * 40)
		print("STUDENT REPORT")
		print("=" * 40)

		for key, value in report.items():
			print(f"{key}: {value}")

	except ValueError as ve:
		print(f"Input Error: {ve}")

	except TypeError as te:
		print(f"Type Error: {te}")

	except Exception as e:
		print(f"Unexpected Error: {e}")

if __name__ == "__main__":
	main()
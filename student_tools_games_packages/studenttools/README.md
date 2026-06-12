Student Tools Package (Mini System)
# Overview

This Python project is a modular Student Performance Tracking System built using packages and multiple modules. It calculates student grades, tracks attendance, and generates a complete performance report.

The system demonstrates real-world software design using:
+ Modular programming (separate files for different responsibilities)
+ Object-like structured functions (clean separation of logic)
+ Input validation and error handling
+ Exception handling using try, except
+ Data aggregation into a final report

The program collects student scores and attendance data, processes them through dedicated modules, and produces a clean, structured student report.

# Features
* Grade calculation based on multiple subject scores
* Input validation for safe and correct data entry
* Attendance tracking system with percentage calculation
* Automatic grade classification (A–F)
* Pass/Fail status evaluation
* Performance remarks based on combined results
* Fully structured student report generation
* Robust error handling for invalid inputs
* Clean modular architecture using Python packages

## Modules Explained
1. Grade Calculator Module (grade_calculator.py)
Handles all academic score processing.

### Responsibilities:
- Validates student scores
- Calculates average score
- Converts average into letter grade
- Determines pass/fail status

### Key Rules:
- Scores must be between 0 and 100
- All scores must be numeric
- Empty score lists are not allowed

2. Attendance Tracker Module (attendance_tracker.py)
Manages student attendance calculations.

### Responsibilities:
- Calculates attendance percentage
- Validates attendance inputs
- Classifies attendance status

### Attendance Status Rules:
- 75% and above → Good Standing
- 50% to 74% → Warning
- Below 50% → Poor Attendance

3. Performance Summary Module (performance_summary.py)
Combines academic and attendance results into a final report.

### Responsibilities:
- Generates performance remarks
- Builds structured student report dictionary

### Remark Logic:
- Grade A + ≥80% attendance → Outstanding Performance
- Grade B/C + ≥75% attendance → Good Performance
- Grade D/F → Needs Academic Improvement
- Otherwise → Average Performance

4. Main Program (student_main.py)
This is the entry point of the system.

### Responsibilities:
- Collects user input safely
- Calls functions from all modules
- Processes grades and attendance
- Generates final report
- Displays formatted output

### Safety Features:
- Handles invalid input (letters instead of numbers, empty names, etc.)
- Graceful handling of keyboard interruption (Ctrl + C)
- Prevents invalid score entry (ensures 0–100 range)

# Technologies Used
- Python 3

# Required Libraries
No external libraries are required.

This project uses only Python built-in features:
- input()
- Exception handling (try, except)
- Basic data types (list, tuple, dict)

# How to Run the Program
1. Navigate into the project folder
cd student_tools_games_packages
2. Run the main script
python student_main.py

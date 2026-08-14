import pandas as pd

class PerformanceAnalytics:
    """Perform analytics on student examination results."""

    def __init__(self, results):
        self.data = pd.DataFrame(results)

    def validate_data(self):
        """Validate the structure of the input data."""

        required_columns = {
            "student_id",
            "student_name",
            "course_code",
            "score",
            "credit_unit",
        }

        missing_columns = required_columns - set(self.data.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        if self.data.empty:
            raise ValueError("No result data was provided.")

        if self.data["score"].isnull().any():
            raise ValueError("Score cannot contain missing values.")

        if self.data["credit_unit"].isnull().any():
            raise ValueError(
                "Credit unit cannot contain missing values."
            )

        if ((self.data["score"] < 0) |
                (self.data["score"] > 100)).any():
            raise ValueError(
                "Scores must be between 0 and 100."
            )

        if (self.data["credit_unit"] <= 0).any():
            raise ValueError(
                "Credit units must be greater than zero."
            )

    def calculate_student_statistics(self):
        """
        Calculate performance statistics for each student.
        """

        self.validate_data()

        data = self.data.copy()

        data["grade_point"] = data["score"].apply(
            self._get_grade_point
        )

        data["quality_point"] = (
            data["grade_point"] * data["credit_unit"]
        )

        statistics = (
            data.groupby(
                ["student_id", "student_name"],
                as_index=False
            )
            .agg(
                total_credit_units=("credit_unit", "sum"),
                total_quality_points=("quality_point", "sum"),
                average_score=("score", "mean"),
            )
        )

        statistics["gpa"] = (
            statistics["total_quality_points"]
            / statistics["total_credit_units"]
        ).round(2)

        statistics["average_score"] = (
            statistics["average_score"].round(2)
        )

        return statistics

    def rank_students(self):
        """Rank students according to GPA."""

        statistics = self.calculate_student_statistics()

        statistics["rank"] = (
            statistics["gpa"]
            .rank(
                method="min",
                ascending=False
            )
            .astype(int)
        )

        return statistics.sort_values(
            by=["rank", "student_name"]
        ).reset_index(drop=True)

    def class_average(self):
        """Return the average score for the entire class."""

        self.validate_data()

        return round(
            self.data["score"].mean(),
            2
        )

    def pass_rate(self):
        """Return the percentage of students who passed."""

        self.validate_data()

        passed = self.data["score"] >= 40

        return round(
            passed.mean() * 100,
            2
        )

    def failure_rate(self):
        """Return the percentage of students who failed."""

        self.validate_data()

        failed = self.data["score"] < 40

        return round(
            failed.mean() * 100,
            2
        )

    def course_statistics(self):
        """Calculate performance statistics by course."""

        self.validate_data()

        statistics = (
            self.data
            .groupby("course_code", as_index=False)
            .agg(
                average_score=("score", "mean"),
                highest_score=("score", "max"),
                lowest_score=("score", "min"),
                number_of_students=("student_id", "count"),
            )
        )

        statistics["average_score"] = (
            statistics["average_score"].round(2)
        )

        return statistics

    def calculate_semester_gpa(
    self,
    student_id,
    semester,
    session,
):
        """Calculate GPA for one student in one semester/session."""

        self.validate_data()

        student_data = self.data[
            (self.data["student_id"] == student_id)
        ].copy()

        if student_data.empty:
            raise ValueError(
                "Student has no results."
            )

        if "semester" not in student_data.columns:
            raise ValueError(
                "Semester information is required."
            )

        if "session" not in student_data.columns:
            raise ValueError(
                "Session information is required."
            )

        student_data = student_data[
            (student_data["semester"] == semester)
            &
            (student_data["session"] == session)
        ]

        if student_data.empty:
            raise ValueError(
                "No results found for the specified "
                "semester and session."
            )

        student_data["grade_point"] = (
            student_data["score"]
            .apply(self._get_grade_point)
        )

        student_data["quality_point"] = (
            student_data["grade_point"]
            * student_data["credit_unit"]
        )

        total_quality_points = (
            student_data["quality_point"].sum()
        )

        total_credit_units = (
            student_data["credit_unit"].sum()
        )

        if total_credit_units <= 0:
            raise ValueError(
                "Total credit units must be greater than zero."
            )

        return round(
            total_quality_points
            / total_credit_units,
            2,
        )

    def calculate_cgpa(self, student_id):
            """
            Calculate cumulative GPA across all
            semesters and sessions.
            """

            self.validate_data()

            student_data = self.data[
                self.data["student_id"] == student_id
            ].copy()

            if student_data.empty:
                raise ValueError(
                    "Student has no results."
                )

            student_data["grade_point"] = (
                student_data["score"]
                .apply(self._get_grade_point)
            )

            student_data["quality_point"] = (
                student_data["grade_point"]
                * student_data["credit_unit"]
            )

            total_quality_points = (
                student_data["quality_point"].sum()
            )

            total_credit_units = (
                student_data["credit_unit"].sum()
            )

            if total_credit_units <= 0:
                raise ValueError(
                    "Total credit units must be greater than zero."
                )

            return round(
                total_quality_points
                / total_credit_units,
                2,
            )

    def academic_history(self, student_id):
        """
        Return semester-by-semester performance
        for a student.
        """

        self.validate_data()

        student_data = self.data[
            self.data["student_id"] == student_id
        ].copy()

        if student_data.empty:
            raise ValueError(
                "Student has no results."
            )

        if "semester" not in student_data.columns:
            raise ValueError(
                "Semester information is required."
            )

        if "session" not in student_data.columns:
            raise ValueError(
                "Session information is required."
            )

        records = []

        grouped = student_data.groupby(
            ["session", "semester"]
        )

        for (session, semester), group in grouped:

            group = group.copy()

            group["grade_point"] = (
                group["score"]
                .apply(self._get_grade_point)
            )

            group["quality_point"] = (
                group["grade_point"]
                * group["credit_unit"]
            )

            total_credit_units = (
                group["credit_unit"].sum()
            )

            total_quality_points = (
                group["quality_point"].sum()
            )

            if total_credit_units <= 0:
                continue

            gpa = round(
                total_quality_points
                / total_credit_units,
                2,
            )

            records.append(
                {
                    "session": session,
                    "semester": semester,
                    "total_credit_units":
                        total_credit_units,
                    "total_quality_points":
                        total_quality_points,
                    "gpa": gpa,
                }
            )

        return records

    @staticmethod
    def _get_grade_point(score):
        """Convert a score into a grade point."""

        if score >= 70:
            return 5.0

        if score >= 60:
            return 4.0

        if score >= 50:
            return 3.0

        if score >= 45:
            return 2.0

        if score >= 40:
            return 1.0

        return 0.0

    
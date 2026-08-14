import pandas as pd

from app.analytics.performance import PerformanceAnalytics


class AdvancedPerformanceAnalytics:
    """Advanced analysis of student performance."""

    def __init__(self, results):
        self.data = pd.DataFrame(results)

        self.analytics = PerformanceAnalytics(
            results
        )

    def _validate(self):
        """Validate the input data."""

        self.analytics.validate_data()

        required_columns = {
            "student_id",
            "student_name",
            "course_code",
            "score",
            "credit_unit",
        }

        missing_columns = (
            required_columns - set(self.data.columns)
        )

        if missing_columns:
            raise ValueError(
                f"Missing columns: "
                f"{sorted(missing_columns)}"
            )

    def grade_distribution(self):
        """Return the distribution of grades."""

        self._validate()

        data = self.data.copy()

        data["grade"] = data["score"].apply(
            self._get_grade
        )

        distribution = (
            data["grade"]
            .value_counts()
            .sort_index()
        )

        return distribution.to_dict()

    def course_performance(self):
        """
        Analyse performance by course.
        """

        self._validate()

        data = self.data.copy()

        statistics = (
            data.groupby("course_code")
            .agg(
                average_score=("score", "mean"),
                highest_score=("score", "max"),
                lowest_score=("score", "min"),
                total_students=("student_id", "count"),
                passed_students=(
                    "score",
                    lambda scores: (
                        scores >= 40
                    ).sum()
                ),
            )
            .reset_index()
        )

        statistics["average_score"] = (
            statistics["average_score"]
            .round(2)
        )

        statistics["pass_rate"] = (
            statistics["passed_students"]
            / statistics["total_students"]
            * 100
        ).round(2)

        statistics["failure_rate"] = (
            100 - statistics["pass_rate"]
        ).round(2)

        return statistics

    def weakest_courses(self, limit=5):
        """
        Return courses with the lowest
        average performance.
        """

        statistics = self.course_performance()

        return (
            statistics
            .sort_values("average_score")
            .head(limit)
            .reset_index(drop=True)
        )

    def strongest_courses(self, limit=5):
        """
        Return courses with the highest
        average performance.
        """

        statistics = self.course_performance()

        return (
            statistics
            .sort_values(
                "average_score",
                ascending=False,
            )
            .head(limit)
            .reset_index(drop=True)
        )

    def student_performance(self, student_id):
        """Analyse an individual student's performance."""

        self._validate()

        student_data = self.data[
            self.data["student_id"] == student_id
        ].copy()

        if student_data.empty:
            raise ValueError(
                "Student has no results."
            )

        student_data["grade"] = (
            student_data["score"]
            .apply(self._get_grade)
        )

        strongest = student_data.loc[
            student_data["score"].idxmax()
        ]

        weakest = student_data.loc[
            student_data["score"].idxmin()
        ]

        return {
            "student_id": student_id,
            "student_name": (
                student_data.iloc[0]["student_name"]
            ),
            "average_score": round(
                student_data["score"].mean(),
                2,
            ),
            "highest_score": float(
                student_data["score"].max()
            ),
            "lowest_score": float(
                student_data["score"].min()
            ),
            "strongest_course": (
                strongest["course_code"]
            ),
            "weakest_course": (
                weakest["course_code"]
            ),
            "gpa": self.analytics.calculate_cgpa(
                student_id
            ),
        }

    def at_risk_students(
        self,
        threshold=2.0,
    ):
        """
        Identify students whose CGPA is
        below the specified threshold.
        """

        self._validate()

        students = []

        for student_id in (
            self.data["student_id"]
            .unique()
        ):
            try:
                cgpa = (
                    self.analytics
                    .calculate_cgpa(student_id)
                )

                student_name = self.data[
                    self.data["student_id"]
                    == student_id
                ].iloc[0]["student_name"]

                if cgpa < threshold:
                    students.append(
                        {
                            "student_id": int(
                                student_id
                            ),
                            "student_name": (
                                student_name
                            ),
                            "cgpa": cgpa,
                            "status": "AT_RISK",
                        }
                    )

            except ValueError:
                continue

        return students

    def performance_trend(self, student_id):
        """
        Determine whether a student's
        performance is improving or declining.
        """

        self._validate()

        if "semester" not in self.data.columns:
            raise ValueError(
                "Semester information is required."
            )

        if "session" not in self.data.columns:
            raise ValueError(
                "Session information is required."
            )

        history = (
            self.analytics
            .academic_history(student_id)
        )

        if len(history) < 2:
            return {
                "student_id": student_id,
                "trend": "INSUFFICIENT_DATA",
                "change": None,
            }

        previous_gpa = history[-2]["gpa"]
        current_gpa = history[-1]["gpa"]

        change = round(
            current_gpa - previous_gpa,
            2,
        )

        if change > 0:
            trend = "IMPROVING"

        elif change < 0:
            trend = "DECLINING"

        else:
            trend = "STABLE"

        return {
            "student_id": student_id,
            "previous_gpa": previous_gpa,
            "current_gpa": current_gpa,
            "change": change,
            "trend": trend,
        }

    @staticmethod
    def _get_grade(score):
        """Convert a score to a letter grade."""

        if score >= 70:
            return "A"

        if score >= 60:
            return "B"

        if score >= 50:
            return "C"

        if score >= 45:
            return "D"

        if score >= 40:
            return "E"

        return "F"
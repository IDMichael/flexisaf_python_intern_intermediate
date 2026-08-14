from typing import Any


class AIInsightService:
    """
    Generates human-readable performance insights
    from verified analytics.

    The AI layer must not calculate academic results.
    """

    def generate_insight(
        self,
        student_analysis: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generate an explanation from verified
        student performance data.
        """

        student_name = student_analysis[
            "student_name"
        ]

        average_score = student_analysis[
            "average_score"
        ]

        highest_score = student_analysis[
            "highest_score"
        ]

        lowest_score = student_analysis[
            "lowest_score"
        ]

        strongest_course = student_analysis[
            "strongest_course"
        ]

        weakest_course = student_analysis[
            "weakest_course"
        ]

        cgpa = student_analysis["gpa"]

        reasons = []

        # Check the student's overall performance.
        if average_score < 50:
            reasons.append(
                "The student's overall average score "
                "is below the passing range."
            )

        elif average_score < 60:
            reasons.append(
                "The student's overall average score "
                "is relatively low."
            )

        # Check for a genuinely weak course.
        if lowest_score < 60:
            reasons.append(
                f"The weakest recorded course is "
                f"{weakest_course}."
            )

        # Check for a failing score.
        if lowest_score < 40:
            reasons.append(
                "The student has at least one course "
                "with a failing score."
            )

        # Check the CGPA.
        if cgpa < 2.0:
            reasons.append(
                "The student's cumulative GPA indicates "
                "a need for academic improvement."
            )

        # Generate the explanation.
        if reasons:
            attention_message = (
                "Possible areas requiring attention: "
                + " ".join(reasons)
            )
        else:
            attention_message = (
                "No major academic warning"
            )

        explanation = (
            f"{student_name}'s current academic "
            f"performance has a CGPA of {cgpa:.2f}. "
            f"The strongest recorded course is "
            f"{strongest_course}, while the weakest "
            f"is {weakest_course}. "
            f"{attention_message}."
        )

        recommendations = self.generate_recommendations(
            student_analysis
        )

        return {
            "student_id": student_analysis[
                "student_id"
            ],
            "student_name": student_name,
            "cgpa": cgpa,
            "average_score": average_score,
            "strongest_course": strongest_course,
            "weakest_course": weakest_course,
            "insight": explanation,
            "reasons": reasons,
            "recommendations": recommendations,
        }

    def generate_recommendations(
        self,
        student_analysis: dict[str, Any],
    ) -> list[str]:
        """
        Generate deterministic academic recommendations
        from verified performance information.
        """

        recommendations = []

        average_score = student_analysis[
            "average_score"
        ]

        lowest_score = student_analysis[
            "lowest_score"
        ]

        cgpa = student_analysis["gpa"]

        weakest_course = student_analysis[
            "weakest_course"
        ]

        if average_score < 50:
            recommendations.append(
                "Review the student's study strategy "
                "and seek academic support."
            )

        elif average_score < 60:
            recommendations.append(
                "Increase revision time and focus on "
                "topics where scores are lowest."
            )

        if lowest_score < 40:
            recommendations.append(
                f"Give additional attention to "
                f"{weakest_course}."
            )

        if cgpa < 2.0:
            recommendations.append(
                "Consider academic advising and a "
                "structured improvement plan."
            )

        if not recommendations:
            recommendations.append(
                "Maintain the current study strategy "
                "while continuing to monitor performance."
            )

        return recommendations
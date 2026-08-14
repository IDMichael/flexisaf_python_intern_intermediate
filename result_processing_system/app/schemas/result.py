from pydantic import BaseModel, Field


class ResultCreate(BaseModel):
    """Data required to create a result."""

    student_id: int = Field(gt=0)

    course_id: int = Field(gt=0)

    score: float = Field(
        ge=0,
        le=100
    )

    semester: str = Field(
        min_length=1,
        max_length=30
    )

    session: str = Field(
        min_length=1,
        max_length=20
    )

class ResultUpdate(BaseModel):
    """Data required to update a student result."""

    student_id: int = Field(
        gt=0
    )

    course_id: int = Field(
        gt=0
    )

    score: float = Field(
        ge=0,
        le=100
    )

    semester: str = Field(
        min_length=1,
        max_length=20
    )

    session: str = Field(
        min_length=1,
        max_length=20
    )

class ResultResponse(BaseModel):
    """Result returned by the API."""

    id: int
    student_id: int
    course_id: int
    score: float
    semester: str
    session: str
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    """Data required to create a student."""

    student_number: str = Field(
        min_length=1,
        max_length=50
    )

    name: str = Field(
        min_length=1,
        max_length=100
    )

    email: str | None = Field(
        default=None,
        max_length=255
    )

    department: str = Field(
        min_length=1,
        max_length=100
    )

    level: int = Field(
        gt=0,
        le=1000
    )

class StudentUpdate(BaseModel):
    """Data required to update a student."""

    student_number: str = Field(
        min_length=1,
        max_length=30
    )

    name: str = Field(
        min_length=1,
        max_length=150
    )

    email: EmailStr

    department: str = Field(
        min_length=1,
        max_length=100
    )

    level: int = Field(
        gt=0,
        le=1000
    )

class StudentResponse(BaseModel):
    """Student returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_number: str
    name: str
    email: str | None
    department: str
    level: int
from pydantic import BaseModel, EmailStr, Field


class StudentRegistrationRequest(BaseModel):
    """Data required to register a student account."""

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    student_number: str = Field(
        min_length=1,
        max_length=50,
    )

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    email: EmailStr

    department: str = Field(
        min_length=1,
        max_length=100,
    )

    level: int = Field(
        ge=100,
        le=600,
    )


class StudentRegistrationResponse(BaseModel):
    """Information returned after successful registration."""

    user_id: int
    student_id: int
    username: str
    role: str

    student_number: str
    name: str
    email: EmailStr
    department: str
    level: int
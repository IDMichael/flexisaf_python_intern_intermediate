from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    """Data required to create a course."""

    course_code: str = Field(
        min_length=1,
        max_length=20
    )

    course_name: str = Field(
        min_length=1,
        max_length=150
    )

    credit_unit: int = Field(
        gt=0,
        le=20
    )

class CourseUpdate(BaseModel):
    """Data required to update a course."""

    course_code: str = Field(
        min_length=1,
        max_length=20
    )

    course_name: str = Field(
        min_length=1,
        max_length=150
    )

    credit_unit: int = Field(
        gt=0,
        le=20
    )
    
class CourseResponse(BaseModel):
    """Course returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    course_code: str
    course_name: str
    credit_unit: int
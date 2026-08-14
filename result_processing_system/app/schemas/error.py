from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard API error response."""

    error: str
    code: str
    message: str
class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "APPLICATION_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


class ResourceNotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str):
        super().__init__(
            message=f"{resource} not found.",
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
        )


class DuplicateResourceError(AppException):
    """Raised when a resource already exists."""

    def __init__(self, resource: str):
        super().__init__(
            message=f"{resource} already exists.",
            status_code=409,
            error_code="DUPLICATE_RESOURCE",
        )


class DatabaseError(AppException):
    """Raised when a database operation fails."""

    def __init__(self, message="A database error occurred."):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
        )


class ValidationError(AppException):
    """Raised when business validation fails."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
        )
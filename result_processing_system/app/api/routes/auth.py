from app.core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
)

from app.schemas.registration import (
    StudentRegistrationRequest,
    StudentRegistrationResponse,
)

from app.services.registration_service import (
    register_student,
)

from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.database.connection import create_connection

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

from app.core.security import (
    create_access_token,
    verify_password,
)

from app.schemas.auth import (
    TokenResponse,
)

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=StudentRegistrationResponse,
    status_code=201,
)
def register(
    registration: StudentRegistrationRequest,
):
    """Register a new student account and profile."""

    try:
        return register_student(
            username=registration.username,
            password=registration.password,
            student_number=registration.student_number,
            name=registration.name,
            email=str(registration.email),
            department=registration.department,
            level=registration.level,
        )

    except DuplicateResourceError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error

    except DatabaseError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

    
@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Authenticate a user and return
    a JWT access token.
    """

    username = form_data.username
    password = form_data.password

    # -----------------------------------------------------
    # Connect to database
    # -----------------------------------------------------

    connection = create_connection()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed.",
        )

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                password_hash,
                role,
                is_active
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        row = cursor.fetchone()

    finally:
        connection.close()

    # -----------------------------------------------------
    # Verify user
    # -----------------------------------------------------

    if row is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    user_id = row[0]
    username = row[1]
    password_hash = row[2]
    role = row[3]
    is_active = row[4]

    # -----------------------------------------------------
    # Check account status
    # -----------------------------------------------------

    if not is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive.",
        )

    # -----------------------------------------------------
    # Verify password
    # -----------------------------------------------------

    if not verify_password(
        password,
        password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    # -----------------------------------------------------
    # Create JWT
    # -----------------------------------------------------

    token = create_access_token(
        data={
            "sub": str(user_id),
            "username": username,
            "role": role,
        },
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
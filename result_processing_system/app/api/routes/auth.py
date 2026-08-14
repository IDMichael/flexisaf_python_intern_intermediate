from datetime import timedelta

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
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
    LoginRequest,
    TokenResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(request: Request):
    """
    Authenticate a user and return
    a JWT access token.

    Supports both:
    - JSON requests
    - OAuth2 form requests from Swagger UI
    """

    content_type = request.headers.get(
        "content-type",
        ""
    )

    # -----------------------------------------------------
    # Read login credentials
    # -----------------------------------------------------

    if "application/json" in content_type:

        body = await request.json()

        data = LoginRequest.model_validate(
            body
        )

        username = data.username
        password = data.password

    else:

        form = await request.form()

        username = form.get("username")
        password = form.get("password")

        if not isinstance(username, str):
            raise HTTPException(
                status_code=422,
                detail="Username is required.",
            )

        if not isinstance(password, str):
            raise HTTPException(
                status_code=422,
                detail="Password is required.",
            )

        data = LoginRequest(
            username=username,
            password=password,
        )

        username = data.username
        password = data.password

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
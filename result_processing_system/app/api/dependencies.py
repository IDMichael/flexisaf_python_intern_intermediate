from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
)

from app.core.security import (
    decode_access_token,
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    """Retrieve the authenticated user."""

    try:
        payload = decode_access_token(
            token
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from error

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token.",
        )

    return payload


def require_admin(
    current_user=Depends(get_current_user),
):
    """Allow only administrators."""

    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Administrator access required.",
        )

    return current_user
from fastapi import APIRouter, Depends

from app.api.dependencies import require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user=Depends(require_admin),
):
    return {
        "message": "Welcome to the admin dashboard.",
        "user": current_user,
    }
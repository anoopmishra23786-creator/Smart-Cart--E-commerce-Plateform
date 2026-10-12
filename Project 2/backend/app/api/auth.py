from fastapi import APIRouter, Depends
from backend.app.dependencies.auth import get_current_user, AuthenticatedUser
from backend.app.schemas.all_schemas import UserProfile
from backend.app.core.supabase_client import get_supabase_client
from backend.app.core.datastore import store

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/me", response_model=UserProfile)
async def get_my_profile(current_user: AuthenticatedUser = Depends(get_current_user)):
    """Return currently authenticated user's profile."""
    # Attempt Supabase query first
    supabase = get_supabase_client()
    if supabase:
        try:
            res = supabase.table("profiles").select("*").eq("id", current_user.id).execute()
            if res.data and len(res.data) > 0:
                p = res.data[0]
                return UserProfile(
                    id=p["id"],
                    email=current_user.email,
                    full_name=p.get("full_name", current_user.full_name),
                    phone=p.get("phone"),
                    is_admin=p.get("is_admin", current_user.is_admin),
                    created_at=p.get("created_at")
                )
        except Exception:
            pass

    # Local fallback
    profiles = store.get_data().get("profiles", [])
    for p in profiles:
        if p["id"] == current_user.id:
            return UserProfile(
                id=p["id"],
                email=p.get("email", current_user.email),
                full_name=p.get("full_name", current_user.full_name),
                phone=p.get("phone"),
                is_admin=p.get("is_admin", current_user.is_admin),
                created_at=p.get("created_at")
            )

    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_admin=current_user.is_admin
    )

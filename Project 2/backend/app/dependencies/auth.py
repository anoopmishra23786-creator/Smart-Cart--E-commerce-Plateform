from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status, Depends
import jwt
from backend.app.core.config import settings
from backend.app.core.supabase_client import get_supabase_client, get_supabase_admin_client
from backend.app.core.datastore import store

class AuthenticatedUser:
    def __init__(self, id: str, email: Optional[str] = None, full_name: str = "", is_admin: bool = False):
        self.id = id
        self.email = email
        self.full_name = full_name
        self.is_admin = is_admin

async def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[AuthenticatedUser]:
    """Extract and verify user from Bearer JWT token if supplied."""
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1].strip()
    if not token:
        return None

    # 1. Check for Demo / Local Test Tokens
    if token.startswith("demo-token-"):
        token_type = token.replace("demo-token-", "")
        if token_type == "admin":
            return AuthenticatedUser(
                id="demo-admin-id",
                email="admin@smartcart.local",
                full_name="SmartCart Administrator",
                is_admin=True
            )
        else:
            return AuthenticatedUser(
                id="demo-user-id",
                email="customer@smartcart.local",
                full_name="Rahul Verma",
                is_admin=False
            )

    # 2. Supabase JWT Validation
    # If SUPABASE_JWT_SECRET is configured, verify signature directly with PyJWT
    if settings.SUPABASE_JWT_SECRET:
        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
            user_id = payload.get("sub")
            email = payload.get("email")
            user_metadata = payload.get("user_metadata", {})
            full_name = user_metadata.get("full_name") or (email.split("@")[0] if email else "User")
            
            # Check Admin status from Supabase profile table or metadata
            is_admin = False
            admin_client = get_supabase_admin_client()
            if admin_client:
                try:
                    res = admin_client.table("profiles").select("is_admin").eq("id", user_id).execute()
                    if res.data and len(res.data) > 0:
                        is_admin = bool(res.data[0].get("is_admin", False))
                except Exception:
                    pass
            else:
                profiles = store.get_data().get("profiles", [])
                for p in profiles:
                    if p["id"] == user_id:
                        is_admin = p.get("is_admin", False)

            return AuthenticatedUser(id=user_id, email=email, full_name=full_name, is_admin=is_admin)
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # 3. Direct verification via Supabase Auth API
    supabase = get_supabase_client()
    if supabase:
        try:
            user_resp = supabase.auth.get_user(token)
            if user_resp and user_resp.user:
                u = user_resp.user
                is_admin = False
                admin_client = get_supabase_admin_client()
                if admin_client:
                    try:
                        res = admin_client.table("profiles").select("is_admin").eq("id", u.id).execute()
                        if res.data and len(res.data) > 0:
                            is_admin = bool(res.data[0].get("is_admin", False))
                    except Exception:
                        pass
                return AuthenticatedUser(
                    id=u.id,
                    email=u.email,
                    full_name=u.user_metadata.get("full_name", u.email.split("@")[0] if u.email else "User"),
                    is_admin=is_admin
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials with Supabase",
                headers={"WWW-Authenticate": "Bearer"},
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(user: Optional[AuthenticatedUser] = Depends(get_current_user_optional)) -> AuthenticatedUser:
    """Requires a valid authenticated user."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_admin(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    """Enforces server-side administrator authorization."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required for this action."
        )
    return user

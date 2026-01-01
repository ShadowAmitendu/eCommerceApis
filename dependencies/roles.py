from fastapi import Depends, HTTPException, status

from dependencies.auth import get_current_user


def require_role(*allowed_roles: str):
    """
    Dependency factory that checks if user has one of the required roles

    Args:
        *allowed_roles: Variable number of role strings (e.g., "admin", "seller")

    Returns:
        A dependency function that validates the user's role

    Example:
        @router.get("/admin-only", dependencies=[Depends(require_role("admin"))])
        def admin_route():
            return {"message": "Admin access"}
    """

    def role_checker(user: dict = Depends(get_current_user)) -> dict:
        user_role = user.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {', '.join(allowed_roles)}"
            )

        return user

    return role_checker

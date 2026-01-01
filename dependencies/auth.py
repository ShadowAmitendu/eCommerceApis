from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import verify_access_token

security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify JWT token and return user payload

    Returns:
        dict: User payload containing sub, user_id, and role

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify required fields exist
    if "sub" not in payload or "user_id" not in payload or "role" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def get_current_active_user(
        current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Get current active user (can be extended to check is_active status)
    """
    return current_user
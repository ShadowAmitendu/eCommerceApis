import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load environment variables from .env file
load_dotenv()

# Use environment variables for secrets - NEVER hardcode them
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

RESET_SECRET_KEY = os.getenv("RESET_SECRET_KEY", "your-reset-secret-change-in-production")

# Use pbkdf2_sha256 - no external dependencies needed, built into passlib
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(password, hashed)


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode["exp"] = expire
    to_encode["iat"] = datetime.now(timezone.utc)

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_reset_token(email: str) -> str:
    """Create a password reset token valid for 15 minutes"""
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        "iat": datetime.now(timezone.utc),
        "type": "reset"
    }
    return jwt.encode(payload, RESET_SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str) -> Optional[str]:
    """Verify a password reset token and return the email"""
    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=[ALGORITHM])

        # Verify it's actually a reset token
        if payload.get("type") != "reset":
            return None

        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


def verify_access_token(token: str) -> Optional[dict]:
    """Verify an access token and return the payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None

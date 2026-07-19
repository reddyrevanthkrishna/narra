from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(data: dict[str, Any]) -> str:
    """
    Create a signed JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT.
    Raises JWTError if the token is invalid or expired.
    """

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    return payload


def verify_token(token: str) -> dict[str, Any]:
    """
    Verify that a JWT is valid and contains the required claims.
    Returns the decoded payload.
    Raises JWTError if validation fails.
    """

    payload = decode_token(token)

    subject = payload.get("sub")

    if subject is None:
        raise JWTError("Token is missing the 'sub' claim.")

    return payload
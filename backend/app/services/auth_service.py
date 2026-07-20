from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserResponse
from app.security.jwt import create_access_token
from app.security.password import verify_password


class AuthService:
    def __init__(self):
        self.repository = UserRepository()

    def authenticate_user(
        self,
        db: Session,
        login: LoginRequest,
    ) -> LoginResponse:
        user = self.repository.get_by_email(
            db,
            login.email,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(
            login.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
            }
        )

        return LoginResponse(
            message="Login successful.",
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )
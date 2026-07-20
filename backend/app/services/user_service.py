from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.security.password import hash_password


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(
        self,
        db: Session,
        user: UserCreate,
    ) -> User:
        existing_user = self.repository.get_by_email(
            db,
            user.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered.",
            )

        db_user = User(
            email=user.email,
            password_hash=hash_password(user.password),
        )

        db_user.profile = UserProfile(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )

        self.repository.create(
            db,
            db_user,
        )

        db.commit()
        db.refresh(db_user)

        return db_user
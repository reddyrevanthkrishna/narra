from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, db: Session, user: UserCreate):
        existing_user = self.repository.get_by_email(db, user.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered.",
            )

        hashed_password = hash_password(user.password)

        db_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
        )

        return self.repository.create(db, db_user)
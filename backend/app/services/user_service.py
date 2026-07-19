from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, db: Session, user: UserCreate):
        return self.repository.create(db, user)
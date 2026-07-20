from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums import UserRole


class UserProfileResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    bio: str | None
    avatar_url: str | None
    phone: str | None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    profile: UserProfileResponse

    model_config = ConfigDict(from_attributes=True)
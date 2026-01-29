from uuid import UUID
from datetime import datetime
from typing import Optional
from app.schemas.base import ORMBase

class UserBase(ORMBase):
    full_name: str
    email: str
    phone: str
    auth_provider: str
    oauth_id: str
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password_hash: Optional[str] = None


class UserUpdate(ORMBase):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    user_id: UUID
    version_no: int

    effective_start_dt: datetime
    effective_end_dt: Optional[datetime]

    created_at: Optional[datetime]
    updated_at: datetime

class UserInDB(UserRead):
    password_hash: Optional[str]

    
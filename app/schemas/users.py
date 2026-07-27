from datetime import datetime
from uuid     import UUID

from pydantic import BaseModel
from pydantic import EmailStr

class UserBase(BaseModel):
    name:  str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id:         UUID
    created_at: datetime

class UserUpdate(BaseModel):
    name:     str      | None = None
    email:    EmailStr | None = None
    password: str      | None = None

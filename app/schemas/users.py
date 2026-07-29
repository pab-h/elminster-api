from datetime import datetime
from uuid     import UUID

from pydantic import BaseModel
from pydantic import EmailStr

class UserBaseSchema(BaseModel):
    name:  str
    email: EmailStr

class UserCreateSchema(UserBaseSchema):
    password: str

class UserReadSchema(UserBaseSchema):
    id:         UUID
    created_at: datetime

class UserUpdateSchema(BaseModel):
    name:     str      | None = None
    email:    EmailStr | None = None
    password: str      | None = None

from sqlmodel import SQLModel
from sqlmodel import Field

from datetime import datetime
from datetime import timezone

from uuid import UUID
from uuid import uuid4

from app.env import settings

class User(SQLModel, table = True):
    id:         UUID     = Field(default_factory = uuid4, primary_key = True)
    name:       str
    password:   str
    created_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))
    
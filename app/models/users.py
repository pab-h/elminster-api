from sqlmodel import SQLModel
from sqlmodel import Field
from sqlmodel import Relationship

from datetime import datetime
from datetime import timezone

from uuid import UUID
from uuid import uuid4

from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Board

class User(SQLModel, table = True):
    id:         UUID     = Field(default_factory = uuid4, primary_key = True)
    email:      str      = Field(unique = True)
    name:       str
    password:   str
    created_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))

    boards: List["Board"] = Relationship(back_populates = "master")
    
from sqlmodel import SQLModel
from sqlmodel import Field
from sqlmodel import Relationship

from datetime import datetime
from datetime import timezone

from uuid import UUID
from uuid import uuid4

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User

class Board(SQLModel, table = True):
    id:          UUID     = Field(default_factory = uuid4, primary_key = True)
    master_id:   UUID     = Field(foreign_key = "user.id")
    title:       str
    description: str      = Field(nullable = True)
    wallpaper:   str      = Field(nullable = True)
    created_at:  datetime = Field(default_factory = lambda: datetime.now(timezone.utc))

    master: "User" = Relationship(back_populates = "boards")
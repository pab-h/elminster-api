from uuid     import UUID
from pydantic import BaseModel
from datetime import datetime

class BoardBaseSchema(BaseModel):
    title:       str
    description: str | None

class BoardCreateSchema(BoardBaseSchema):
    pass

class BoardReadSchema(BoardBaseSchema):
    id:         UUID
    master_id:  UUID
    wallpaper:  str | None
    created_at: datetime
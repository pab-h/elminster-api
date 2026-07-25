from typing import Generator

from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine
from sqlmodel import text

from app.env import settings

import app.models

engine = create_engine(
    url  = settings.database_url
)

def get_db_session() -> Generator[Session, None, None]:
    
    with Session(engine) as session:
        yield session

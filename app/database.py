from typing import Generator

from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine

from app.env import settings

engine = create_engine(
    url  = settings.database_url,
    echo = True
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

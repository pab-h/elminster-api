from typing import Generator

from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine
from sqlmodel import text

from app.env import settings

from app.models.users     import User
from app.models.documents import Document
from app.models.documents import DocumentChunks

engine = create_engine(
    url  = settings.database_url
)

def create_db_and_tables():
    
    with Session(engine) as session:
        session.exec(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        session.commit()
        
    SQLModel.metadata.create_all(engine)

def get_db_session() -> Generator[Session, None, None]:
    
    with Session(engine) as session:
        yield session

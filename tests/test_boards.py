import pytest

from uuid import uuid4

from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine

from sqlmodel.pool import StaticPool

from app.schemas import UserCreateSchema
from app.schemas import BoardCreateSchema

from app.services.users  import create_user
from app.services.boards import create_board

from app.services.exceptions import UserNotFoundException


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_board_success(session: Session):
    user_in = UserCreateSchema(name="Master User", email="master@example.com", password="password123")
    user = create_user(user_in, session)

    board_in = BoardCreateSchema(title="RPG Campaign", description="Main campaign board")
    board = create_board(board_in, user.id, session)

    assert board.id is not None
    assert board.title == "RPG Campaign"
    assert board.description == "Main campaign board"
    assert board.master_id == user.id


def test_create_board_without_description_success(session: Session):
    user_in = UserCreateSchema(name="Master User", email="master2@example.com", password="password123")
    user = create_user(user_in, session)

    board_in = BoardCreateSchema(title="RPG Campaign Minimal", description=None)
    board = create_board(board_in, user.id, session)

    assert board.id is not None
    assert board.title == "RPG Campaign Minimal"
    assert board.description is None
    assert board.master_id == user.id


def test_create_board_user_not_found_raises_exception(session: Session):
    board_in = BoardCreateSchema(title="Orphan Board", description="Board without valid master")

    with pytest.raises(UserNotFoundException):
        create_board(board_in, uuid4(), session)
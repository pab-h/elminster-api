import pytest

from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine

from sqlmodel.pool import StaticPool

from app.schemas import LoginSchema
from app.schemas import UserCreateSchema

from app.services.users          import create_user
from app.services.authentication import login  

from app.services.exceptions import UserNotFoundException
from app.services.exceptions import IncorrectPasswordException

@pytest.fixture(name = "session")
def session_fixture():
    
    engine = create_engine(
        "sqlite://", 
        connect_args = {"check_same_thread": False}, 
        poolclass    = StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_login_success(session: Session):

    user_in = UserCreateSchema(name="Grace", email="grace@example.com", password="correct_password")
    create_user(user_in, session)

    login_data = LoginSchema(email="grace@example.com", password="correct_password")
    token_response = login(login_data, session)

    assert token_response is not None
    assert token_response.token_type == "bearer"
    assert isinstance(token_response.token, str)
    assert len(token_response.token) > 0


def test_login_incorrect_password_raises_exception(session: Session):

    user_in = UserCreateSchema(name="Grace", email="grace@example.com", password="correct_password")
    create_user(user_in, session)

    login_data = LoginSchema(email="grace@example.com", password="wrong_password")

    with pytest.raises(IncorrectPasswordException):
        login(login_data, session)


def test_login_user_not_found_raises_exception(session: Session):

    login_data = LoginSchema(email="nonexistent@example.com", password="any_password")

    with pytest.raises(UserNotFoundException):
        login(login_data, session)

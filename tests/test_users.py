import pytest

from uuid import uuid4

from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine

from sqlmodel.pool import StaticPool

from app.schemas import UserCreateSchema
from app.schemas import UserUpdateSchema

from app.services.users import create_user
from app.services.users import find_user_by_id
from app.services.users import find_user_by_email
from app.services.users import update_user
from app.services.users import delete_user

from app.services.exceptions import UserEmailAlredyExistsException
from app.services.exceptions import UserNotFoundException

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

def test_create_user_success(session: Session):
    user_in = UserCreateSchema(name="Alice", email="alice@example.com", password="secretpassword")
    user = create_user(user_in, session)

    assert user.id is not None
    assert user.email == "alice@example.com"

def test_create_user_duplicate_email_raises_exception(session: Session):
    user_in = UserCreateSchema(name="Alice", email="alice@example.com", password="secretpassword")
    create_user(user_in, session)

    with pytest.raises(UserEmailAlredyExistsException):
        create_user(user_in, session)


def test_find_user_not_found_raises_exception(session: Session):
    
    with pytest.raises(UserNotFoundException):
        find_user_by_id(uuid4(), session)

def test_find_user_success(session: Session):
    user_in = UserCreateSchema(name="Bob", email="bob@example.com", password="password123")
    created_user = create_user(user_in, session)

    found_user = find_user_by_id(created_user.id, session)

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == "bob@example.com"


def test_update_user_success(session: Session):
    user_in = UserCreateSchema(name="Charlie", email="charlie@example.com", password="password123")
    created_user = create_user(user_in, session)

    update_data = UserUpdateSchema(name="Charlie Updated")
    updated_user = update_user(created_user.id, update_data, session)

    assert updated_user.name == "Charlie Updated"
    assert updated_user.email == "charlie@example.com"  

def test_update_user_not_found_raises_exception(session: Session):
    update_data = UserUpdateSchema(name="Ghost")
    
    with pytest.raises(UserNotFoundException):
        update_user(uuid4(), update_data, session)

def test_update_user_duplicate_email_raises_exception(session: Session):

    user1 = create_user(UserCreateSchema(name="User 1", email="u1@example.com", password="pwd"), session)
    user2 = create_user(UserCreateSchema(name="User 2", email="u2@example.com", password="pwd"), session)

    update_data = UserUpdateSchema(email="u1@example.com")
    
    with pytest.raises(UserEmailAlredyExistsException):
        update_user(user2.id, update_data, session)


def test_delete_user_success(session: Session):
    user_in = UserCreateSchema(name="Dave", email="dave@example.com", password="password123")
    created_user = create_user(user_in, session)

    delete_user(created_user.id, session)

    with pytest.raises(UserNotFoundException):
        find_user_by_id(created_user.id, session)

def test_delete_user_not_found_raises_exception(session: Session):
    with pytest.raises(UserNotFoundException):
        delete_user(uuid4(), session)

def test_find_user_by_email_success(session: Session):
    user_in = UserCreateSchema(name="Eve", email="eve@example.com", password="password123")
    created_user = create_user(user_in, session)

    found_user = find_user_by_email("eve@example.com", session)

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == "eve@example.com"

def test_find_user_by_email_not_found_raises_exception(session: Session):
    with pytest.raises(UserNotFoundException):
        find_user_by_email("nonexistent@example.com", session)

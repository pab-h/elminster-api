from uuid import UUID

from sqlmodel import Session
from sqlmodel import select

from app.models  import User

from app.schemas import UserCreate
from app.schemas import UserRead
from app.schemas import UserUpdate

from app.services.exceptions import UserEmailAlredyExistsException
from app.services.exceptions import UserNotFoundException

def create_user(
    user_data: UserCreate,
    session:   Session 
) -> UserRead:
    
    user_found = session.exec(
        select(User).where(User.email == user_data.email)
    ).one_or_none()

    if user_found:
        raise UserEmailAlredyExistsException()

    user = User(
        name     = user_data.name,
        email    = user_data.email,
        password = user_data.password,
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def find_user(
    id:      UUID,
    session: Session 
) -> UserRead:
    
    user = session.get(User, id)

    if not user:
        raise UserNotFoundException()
    
    return user    

def find_all_user(
    session: Session 
) -> list[UserRead]:
    
    users = session.exec(select(User)).all()

    return users

def update_user(
    id:        UUID,
    user_data: UserUpdate,
    session:   Session 
) -> UserRead:
    
    user = session.get(User, id)

    if not user:
        raise UserNotFoundException()

    user_dict = user_data.model_dump(exclude_unset=True)

    if "email" in user_dict and user_dict["email"] != user.email:

        email_exists = session.exec(
            select(User).where(User.email == user_dict["email"])
        ).one_or_none()

        if email_exists:
            raise UserEmailAlredyExistsException()
    
    for key, value in user_dict.items():
        if key != "id": 
            setattr(user, key, value)
            
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user    

def delete_user(
    id:      UUID,
    session: Session 
):
    user = session.get(User, id)
    
    if not user:
        raise UserNotFoundException()
        
    session.delete(user)
    session.commit()

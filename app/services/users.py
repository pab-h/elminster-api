from uuid import UUID

from sqlmodel import Session
from sqlmodel import select

from app.models  import User

from app.schemas import UserCreateSchema
from app.schemas import UserUpdateSchema

from app.services.exceptions import UserEmailAlredyExistsException
from app.services.exceptions import UserNotFoundException

def create_user(
    user_data: UserCreateSchema,
    session:   Session 
) -> User:
    
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

def find_user_by_id(
    id:      UUID,
    session: Session 
) -> User:
    
    user = session.get(User, id)

    if not user:
        raise UserNotFoundException()
    
    return user    

def find_user_by_email(
    email:   str,
    session: Session 
) -> User:
    
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        raise UserNotFoundException()
    
    return user   

def update_user(
    id:        UUID,
    user_data: UserUpdateSchema,
    session:   Session 
) -> User:
    
    user = session.get(User, id)

    if not user:
        raise UserNotFoundException()

    user_dict = user_data.model_dump(exclude_unset=True)

    if "email" in user_dict and user_dict["email"] != user.email:

        email_exists = session.exec(
            select(User).where(User.email == user_dict["email"])
        ).first()

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

from uuid import UUID

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException

from sqlmodel import Session
from sqlmodel import select

from app.models   import User
from app.database import get_db_session

from app.schemas import UserCreate
from app.schemas import UserRead
from app.schemas import UserUpdate

router = APIRouter(
    tags   = ["Users"],
    prefix = "/users"
)

@router.post("/", status_code = status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session:   Session = Depends(get_db_session)
) -> UserRead:

    user = User(
        name     = user_data.name,
        email    = user_data.email,
        password = user_data.name,
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.get("/{id}", status_code = status.HTTP_200_OK)
async def find_user(
    id:      UUID,
    session: Session = Depends(get_db_session)
) -> UserRead:
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail      = "User not found"
        )
    return user    

@router.get("/", status_code = status.HTTP_200_OK)
async def find_all_user(
    session: Session = Depends(get_db_session)
) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return users

@router.put("/{id}", status_code = status.HTTP_200_OK)
async def update_user(
    id:        UUID,
    user_data: UserUpdate,
    session:   Session = Depends(get_db_session)
) -> UserRead:
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail      = "User not found"
        )
    
    user_dict = user_data.model_dump(exclude_unset=True)
    for key, value in user_dict.items():
        if key != "id": 
            setattr(user, key, value)
            
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user    

@router.delete("/{id}", status_code = status.HTTP_200_OK)
async def delete_user(
    id:      UUID,
    session: Session = Depends(get_db_session)
):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail      = "User not found"
        )
        
    session.delete(user)
    session.commit()

    return {
        "message": "User successfully removed"
    }
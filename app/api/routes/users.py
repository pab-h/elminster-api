from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlmodel import Session

from app.database import get_db_session

from app.schemas import UserCreateSchema
from app.schemas import UserReadSchema
from app.schemas import UserUpdateSchema

from app.services import users as user_service

from app.api.authentication import get_current_user_id

router = APIRouter(
    tags   = ["Users"], 
    prefix = "/users"
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreateSchema,
    session:   Session = Depends(get_db_session)
) -> UserReadSchema:
    
    return user_service.create_user(
        user_data = user_data, 
        session   = session
    )

@router.get("/{id}", status_code = status.HTTP_200_OK)
def find_user(
    id:      UUID,
    session: Session = Depends(get_db_session)
) -> UserReadSchema:
    
    return user_service.find_user_by_id(
        id      = id, 
        session = session
    )

@router.put("/", status_code = status.HTTP_200_OK)
def update_user(
    user_data: UserUpdateSchema,
    id:        UUID             = Depends(get_current_user_id),
    session:   Session          = Depends(get_db_session)
) -> UserReadSchema:
    
    return user_service.update_user(
        id        = id, 
        user_data = user_data, 
        session   = session
    )

@router.delete("/", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(
    id:      UUID    = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    
    user_service.delete_user(
        id      = id, 
        session = session
    )

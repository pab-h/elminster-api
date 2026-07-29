from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlmodel import Session

from app.database import get_db_session

from app.schemas import LoginSchema
from app.schemas import TokenSchema

from app.services import authentication

router = APIRouter(
    tags   = ["Authentication"], 
    prefix = "/login"
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def login(
    login_data: LoginSchema,
    session:    Session = Depends(get_db_session)
) -> TokenSchema:

    return authentication.login(login_data, session)

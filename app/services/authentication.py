from sqlmodel import Session

from app.schemas import LoginSchema
from app.schemas import TokenSchema

from app.services.users      import find_user_by_email
from app.services.exceptions import IncorrectPasswordException

from app.security import create_jwt_token

def login(
    login_data: LoginSchema,
    session:    Session 
) -> TokenSchema:
    
    user = find_user_by_email(
        email   = login_data.email,
        session = session
    )

    if user.password != login_data.password:
        raise IncorrectPasswordException()

    access_token = create_jwt_token(data = {
        "sub": str(user.id)
    })

    return TokenSchema(
        token      = access_token,
        token_type = "bearer"
    )
    
from fastapi import Depends

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from app.security import get_jwt_token_payload 

from uuid import UUID

bearer_scheme = HTTPBearer()

def get_current_user_id(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> UUID:
    return get_jwt_token_payload(token.credentials)['sub']
import jwt

from datetime import datetime
from datetime import timedelta

from zoneinfo import ZoneInfo

from app.env import settings

def create_jwt_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.now(tz = ZoneInfo('UTC')) + timedelta(
        minutes = settings.jwt_expire_minutes
    )

    to_encode.update({'exp': expire })

    encoded_jwt = jwt.encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm = settings.jwt_algorithm
    )

    return encoded_jwt

def get_jwt_token_payload(token: str) -> dict:

    return jwt.decode(
        token, 
        settings.jwt_secret_key, 
        algorithms = [settings.jwt_algorithm]
    )
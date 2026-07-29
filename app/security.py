from datetime import datetime
from datetime import timedelta

from zoneinfo import ZoneInfo
from jwt      import encode

from app.env import settings

def create_jwt_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.now(tz = ZoneInfo('UTC')) + timedelta(
        minutes = settings.jwt_expire_minutes
    )

    to_encode.update({'exp': expire })

    encoded_jwt = encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm = settings.jwt_algorithm
    )

    return encoded_jwt
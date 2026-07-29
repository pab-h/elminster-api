from pydantic import BaseModel
from pydantic import EmailStr

class LoginSchema(BaseModel):
    email:    EmailStr
    password: str

class TokenSchema(BaseModel):
    token:      str
    token_type: str

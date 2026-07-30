from pydantic import BaseModel

class QueryBodyRequest(BaseModel):
    query: str

class QueryBodyResponse(BaseModel):
    answer: str
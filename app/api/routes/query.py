from uuid import UUID

from typing import Any

from langchain_core.runnables import RunnableSerializable

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException

from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from app.rag.retrieve import get_retrieve_chain

from app.api.authentication import get_current_user_id

router = APIRouter(
    tags   = ["Query"],
    prefix = "/query"
)

class QueryBodyRequest(BaseModel):
    query: str

class QueryBodyResponse(BaseModel):
    answer: str

@router.post("/stream")
def query_stream(
    body:           QueryBodyRequest,
    retrieve_chain: RunnableSerializable[Any, str]  = Depends(get_retrieve_chain),
    id:             UUID                            = Depends(get_current_user_id)
) -> StreamingResponse:
    
    if not body.query.strip():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "The query cannot be empty"
        )

    return StreamingResponse(
        retrieve_chain.stream(body.query),
        media_type = "text/event-stream"
    )

@router.post("/")
def query(
    body:           QueryBodyRequest,
    retrieve_chain: RunnableSerializable[Any, str]  = Depends(get_retrieve_chain),
    id:             UUID                            = Depends(get_current_user_id)
) -> QueryBodyResponse:
    
    if not body.query.strip():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "The query cannot be empty"
        )

    return QueryBodyResponse(
        answer = retrieve_chain.invoke(body.query)
    )

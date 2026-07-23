from typing import Any

from langchain_core.runnables import RunnableSerializable

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException

from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from app.rag.retrieve import get_retrieve_chain

router = APIRouter(
    tags = ["Query"]
)

class QueryBodyRequest(BaseModel):
    query: str

class QueryBodyResponse(BaseModel):
    answer: str

@router.post("/query/stream")
async def query_stream(
    body:           QueryBodyRequest,
    retrieve_chain: RunnableSerializable[Any, str]  = Depends(get_retrieve_chain)
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

@router.post("/query")
async def query(
    body:           QueryBodyRequest,
    retrieve_chain: RunnableSerializable[Any, str]  = Depends(get_retrieve_chain)
) -> QueryBodyResponse:
    
    if not body.query.strip():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "The query cannot be empty"
        )

    return QueryBodyResponse(
        answer = retrieve_chain.invoke(body.query)
    )

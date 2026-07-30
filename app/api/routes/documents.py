import shutil

from typing   import Any
from sqlmodel import Session
from pydantic import BaseModel
from uuid     import UUID

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import HTTPException

from fastapi.responses import StreamingResponse

from app.schemas import QueryBodyRequest
from app.schemas import QueryBodyResponse

from app.models import DocumentState
from app.models import Document

from app.database import get_db_session
from app.workers  import digest_document_task
from app.env      import settings

from app.api.authentication import get_current_user_id
from app.rag.retrieve       import get_retrieve_chain

from langchain_core.runnables import RunnableSerializable

router = APIRouter(
    tags   = ["Documents"],
    prefix = "/documents"
)

class DigestPostResponse(BaseModel):
    document_id: UUID
    status:      DocumentState

@router.post("/digest/", status_code = status.HTTP_201_CREATED)
async def digest_document(
    file:    UploadFile, 
    session: Session = Depends(get_db_session),
    id:      UUID    = Depends(get_current_user_id)
) -> DigestPostResponse:
    
    settings.upload_path.mkdir(
        parents  = True,
        exist_ok = True
    )

    file_path = settings.upload_path / file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail       = f"Could not save file: {str(e)}",
        )
    finally:
        await file.close()

    document = Document(
        filename     = file.filename,
        storage_path = str(file_path),
        status       = DocumentState.PENDING,
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    digest_document_task.delay(document_id = str(document.id))

    return DigestPostResponse(
        document_id = document.id, 
        status      = document.status
    )

@router.post("/query/stream/")
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

@router.post("/query/")
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

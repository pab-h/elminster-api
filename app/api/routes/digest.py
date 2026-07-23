import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException

from sqlmodel import Session

from pydantic import BaseModel
from uuid     import UUID

from app.models   import DocumentState
from app.models   import Document
from app.database import get_db_session
from app.workers  import digest_document_task
from app.env      import settings

router = APIRouter(
    tags = ["Documents"]
)

class DigestPostResponse(BaseModel):
    document_id: UUID
    status:      DocumentState

@router.post("/digest", status_code = status.HTTP_201_CREATED)
async def digest_document(
    file:    UploadFile, 
    session: Session = Depends(get_db_session)
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

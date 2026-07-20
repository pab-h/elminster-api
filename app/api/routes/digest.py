from fastapi import APIRouter
from fastapi import UploadFile


from pydantic   import BaseModel
from uuid       import UUID

from app.models import DocumentState

router = APIRouter(
    tags = ["Documents"]
)

class DigestPostResponse(BaseModel):
    document_id: UUID
    status:      DocumentState

@router.post("/digest")
async def digest_document(file: UploadFile) -> DigestPostResponse:

    return {
        "document_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "status":      "PENDING"
    }


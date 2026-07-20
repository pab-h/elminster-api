from sqlmodel import SQLModel
from sqlmodel import Relationship
from sqlmodel import Field
from sqlmodel import Index

from pydantic import ConfigDict

from typing   import Optional
from typing   import List

from datetime import datetime
from datetime import UTC

from enum import Enum

from uuid import UUID
from uuid import uuid4

from pgvector.sqlalchemy import VECTOR

class DocumentState(str, Enum):
    PENDING    = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED  = "COMPLETED"
    FAILED     = "FAILED"

class Document(SQLModel, table = True):
    id:            UUID          = Field(default_factory = uuid4, primary_key = True)
    filename:      str
    storage_path:  str
    status:        DocumentState = Field(default = DocumentState.PENDING)
    created_at:    datetime      = Field(default_factory = datetime.now(UTC))
    error_message: Optional[str] = Field(default = None)

    chunks: List["DocumentChunks"] = Relationship(back_populates = "document")

class DocumentChunks(SQLModel, table = True):
    id:          UUID        = Field(default_factory = uuid4, primary_key = True)
    content:     str
    document_id: UUID
    embedding:   List[float] = Field(sa_type = VECTOR(768))

    document: Document = Relationship(back_populates = "chunks")

    model_config = ConfigDict(arbitrary_types_allowed = True)

    __table_args__ = (
        Index(
            "idx_document_chunks_embedding",
            "embedding",
            postgresql_using = "hnsw",
            postgresql_ops   = {
                "embedding": "vector_cosine_ops"
            },
        ),
    )
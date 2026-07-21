import logging

from app.models import Document
from app.models import DocumentChunks
from app.models import DocumentState

from app.rag_pipeline import parse_file
from app.rag_pipeline import text_chunking
from app.rag_pipeline import generate_embeddings

from app.database import get_db_session
from app.env      import settings

from pathlib import Path
from uuid    import UUID

from celery  import Celery

celery_app = Celery(
    "tasks", 
    broker  = settings.redis_url, 
    backend = settings.redis_url
)

logger = logging.getLogger(__name__)

@celery_app.task(bind = True, max_retries = 3)
def digest_document_task(self, document_id: str):

    session = next(get_db_session())

    document = session.get(Document, UUID(document_id))

    if not document:

        logger.error(f"Document with ID {document_id} not found.")
        session.close()

        return

    try:

        document.status = DocumentState.PROCESSING
        session.add(document)
        session.commit()

        target_path = Path(document.storage_path)

        logger.info(f"Parsing file: {document.filename}")
        content = parse_file(target_path)

        logger.info(f"Chunking document: {document.filename}")
        chunks = text_chunking(content)

        logger.info(f"Generating embeddings for {len(chunks)} chunks")
        embeddings = generate_embeddings(chunks)

        document_chunks = [
            DocumentChunks(
                content     = chunk_text,
                embedding   = embedding_vector,
                document_id = document.id,
            )
            for chunk_text, embedding_vector in zip(chunks, embeddings)
        ]

        session.add_all(document_chunks)
        document.status = DocumentState.COMPLETED
        session.commit()

        logger.info(f"Successfully processed document {document.filename} (ID: {document.id})")

        return {
            "status":      "COMPLETED", 
            "document_id": str(document.id) 
        }

    except Exception as e:

        logger.error(f"Failed processing document {document.filename}: {str(e)}")
        session.rollback()

        if document.id:
            document.status        = DocumentState.FAILED
            document.error_message = str(e)
            session.add(document)
            session.commit()

        raise e

    finally:
        session.close()

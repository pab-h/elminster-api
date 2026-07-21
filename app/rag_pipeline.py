from pathlib import Path
from typing  import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from markitdown               import MarkItDown
from ollama                   import Client

from app.env import settings

def parse_file(target: Path) -> str:

    md     = MarkItDown()
    result = md.convert_local(target)

    return result.markdown


def text_chunking(text: str) -> List[str]:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size    = 1000, 
        chunk_overlap = 200
    )

    return text_splitter.split_text(text)


def generate_embeddings(chunks: List[str]) -> List[List[float]]:

    client          = Client(host = settings.ollama_url)
    prefixed_chunks = [f"search_document: {chunk}" for chunk in chunks]

    response = client.embed(
        model = settings.embedding_model, 
        input = prefixed_chunks
    )

    return response.embeddings

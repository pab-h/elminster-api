
from typing import List
from typing import Any

from langchain_core.prompts        import ChatPromptTemplate
from langchain_core.runnables      import RunnablePassthrough
from langchain_core.runnables      import RunnableSerializable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents      import Document

from langchain_ollama   import ChatOllama
from langchain_ollama   import OllamaEmbeddings

from langchain_postgres import PGVector

from app.env import settings

def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

def get_vector_store() -> PGVector:

    embeddings = OllamaEmbeddings(
        model    = settings.embedding_model,
        base_url = settings.ollama_url
    )

    vector_store = PGVector(
        embeddings       = embeddings,
        collection_name  = "documents",
        connection       = settings.database_url,
        use_jsonb        = True,
    )
    
    return vector_store

def get_retrieve_chain() -> RunnableSerializable[Any, str]:

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs = { "k": settings.context_length }
    )

    prompt_template = ChatPromptTemplate.from_template(
        """You are a helpful assistant. Use only the provided context below to answer the user's question. 
        If the context does not contain the answer, say that you do not know.

        Context:
        {context}

        Question: {question}
        Answer:"""
    )

    llm = ChatOllama(
        model       = settings.llm_model,
        base_url    = settings.ollama_url,
        temperature = 0,
    )

    retrieve_chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )

    return retrieve_chain

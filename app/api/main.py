from fastapi import FastAPI

from app.ollama_setup import ensure_models_exists

from app.api.routes import digest
from app.api.routes import query

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    await ensure_models_exists()

    yield

app = FastAPI(
    title       = "Elminster API",
    description = "API para servir um sistema de inteligência artificial voltado para a assistência em jogos de RPG de mesa",
    lifespan    = lifespan
)

app.include_router(digest.router)
app.include_router(query.router)

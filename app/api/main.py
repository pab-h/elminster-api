from fastapi import FastAPI

from app.database     import create_db_and_tables
from app.ollama_setup import ensure_models_exists
from app.api.routes   import digest

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()
    await ensure_models_exists()

    yield


app = FastAPI(
    title       = "Elminster API",
    description = "API para servir um sistema de inteligência artificial voltado para a assistência em jogos de RPG de mesa",
    lifespan    = lifespan
)

app.include_router(digest.router)

@app.get("/")
async def root():
    return { "message": "Hello World!" }

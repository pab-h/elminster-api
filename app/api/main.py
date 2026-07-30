from fastapi import FastAPI

from app.ollama_setup import ensure_models_exists

from app.api.routes import users
from app.api.routes import authentication
from app.api.routes import documents

from app.api.exceptions import assign_exception_handlers

def lifespan(app: FastAPI):

    ensure_models_exists()

    yield

app = FastAPI(
    title       = "Elminster API",
    description = "API para servir um sistema de inteligência artificial voltado para a assistência em jogos de RPG de mesa",
    lifespan    = lifespan
)

assign_exception_handlers(app)

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(documents.router)

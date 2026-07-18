from fastapi import FastAPI

from app.database import create_db_and_tables

create_db_and_tables()

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World!" }
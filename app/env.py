from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):

    api_name:      str
    upload_path:   Path
    context_length: int

    ollama_url:      str
    embedding_model: str
    embedding_size:  int
    llm_model:       str

    database_url: str

    redis_host: str
    redis_port: int
    redis_url:  str

    model_config = SettingsConfigDict(
        env_file          = ".env",
        env_file_encoding = "utf-8",
        extra             = "ignore"
    )

settings = Settings()

if __name__ == "__main__":

    print(settings.api_name)

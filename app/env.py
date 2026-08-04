from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):

    api_name:           str
    max_wallpaper_size: int
    context_length:     int

    garage_endpoint:           str
    garage_public_url:         str
    garage_default_bucket:     str
    garage_default_access_key: str
    garage_default_secret_key: str

    jwt_secret_key:     str
    jwt_algorithm:      str
    jwt_expire_minutes: int

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

from logging.config import fileConfig

from alembic    import context
from sqlalchemy import engine_from_config, pool

from sqlmodel import SQLModel

from app.env import settings

from app.models.users     import User
from app.models.documents import Document
from app.models.documents import DocumentChunks

config = context.config

config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def include_name(name, type_, parent_names):
    if type_ == "table":
        return name not in ["langchain_pg_embedding", "langchain_pg_collection"]
    return True

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=include_name,  # <--- ADICIONE AQUI
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_name=include_name,  # <--- ADICIONE AQUI
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

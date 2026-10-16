import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Make project root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# --- Match YOUR import style ---
import config
from database import Base
from models import User  # Add more models here as you create them

config_alembic = context.config

if config_alembic.config_file_name is not None:
    fileConfig(config_alembic.config_file_name)

# --- Build URL exactly like your database.py does ---
DATABASE_URL = (
    f"postgresql+psycopg://{config.DB_USER}:"
    f"{config.DB_PASSWORD}@{config.DB_HOST}:"
    f"{config.DB_PORT}/{config.DB_NAME}"
)
config_alembic.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config_alembic.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config_alembic.get_section(config_alembic.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
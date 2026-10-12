
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

import config

DATABASE_URL = (
    f"postgresql+psycopg://{config.DB_USER}:"
    f"{config.DB_PASSWORD}@{config.DB_HOST}:"
    f"{config.DB_PORT}/{config.DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def check_db_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Db is connected=========================", result)
        return result.scalar()

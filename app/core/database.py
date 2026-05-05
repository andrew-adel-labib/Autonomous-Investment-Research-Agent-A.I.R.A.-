import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

engine = None
SessionLocal = None


def get_database_url():
    if os.getenv("PYTEST_CURRENT_TEST") or os.getenv("ENVIRONMENT") == "test":
        return "sqlite:///./test.db"

    return settings.DATABASE_URL


def init_db():
    global engine, SessionLocal

    if engine is None:
        database_url = get_database_url()

        connect_args = {}
        if database_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}

        engine = create_engine(
            database_url,
            connect_args=connect_args,
            pool_pre_ping=True
        )

        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )

    return engine
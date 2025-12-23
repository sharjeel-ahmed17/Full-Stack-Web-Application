from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import Session, SQLModel
from contextlib import contextmanager

from .config import settings


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,  # Set to True for SQL query logging during development
)


@contextmanager
def get_session():
    """
    Context manager for database sessions.
    Ensures proper cleanup of database connections.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session_dep():
    """
    FastAPI dependency for database sessions.
    """
    with get_session() as session:
        yield session
"""
database.py

This module sets up the SQLAlchemy database engine, sessionmaker, and base class
for ORM models. It provides a dependency function `get_db` to be used with FastAPI
routes for managing database sessions.

Database: SQLite (blog.db)

Also it offers the flexibility to use what ever the database server we want like Postgres, etc.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///blog.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function that yields a database session.

    Ensures that the session is closed after the request is processed.
    Should be used with FastAPI's `Depends()`.

    Example:
        def route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

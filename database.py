"""
database.py
-----------
Configures the SQLAlchemy database engine, session factory, and declarative base.

All models inherit from `Base`. The `SessionLocal` is used to create
per-request database sessions via dependency injection in Controller.py.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

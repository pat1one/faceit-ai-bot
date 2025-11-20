"""
Database configuration and SQLAlchemy setup
"""
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(str(Path(__file__).parent))
from config.settings import settings

# Creation engine
if settings.DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # Use a simple engine configuration for PostgreSQL that matches
    # the manual test (create_engine(settings.DATABASE_URL)) which
    # successfully connects with the current credentials.
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )

# Creation session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

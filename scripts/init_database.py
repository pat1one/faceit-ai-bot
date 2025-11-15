#!/usr/bin/env python3
"""Initialize database with migrations"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import create_engine  # noqa: E402
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from server.config.settings import settings  # noqa: E402
from server.database.models import Base  # noqa: E402


def init_database():
    """Initialize database and run migrations"""
    print("🚀 Initializing database...")

    # Create engine
    engine = create_engine(settings.DATABASE_URL, echo=True)

    try:
        # Create all tables (fallback if migrations fail)
        print("📋 Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")

        # Run migrations
        print("🔄 Running migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("✅ Migrations completed successfully")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

    print("🎉 Database initialization completed!")
    return True


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)

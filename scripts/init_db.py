#!/usr/bin/env python3
"""Database initialization script."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.database import init_db, engine
from app.models import Todo
from app.core.logging import logger


def main():
    """Initialize the database and create tables."""
    try:
        logger.info("Initializing database...")

        # Create all tables
        init_db()

        logger.info("Database initialized successfully")
        logger.info(f"Database URL: {engine.url}")

        # Print created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        logger.info(f"Created tables: {', '.join(tables)}")

        print("\n✓ Database initialization completed successfully")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

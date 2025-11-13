#!/usr/bin/env python3
"""Seed database with sample data."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.database import SessionLocal
from app.models.todo import Todo
from app.core.logging import logger


def seed_todos():
    """Seed the database with sample todos."""
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Todo).count()

        if existing_count > 0:
            logger.info(f"Database already contains {existing_count} todos")
            print(f"\nDatabase already contains {existing_count} todos")
            response = input("Do you want to add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("Skipping seed operation")
                return

        # Sample todo data
        sample_todos = [
            {
                "title": "Set up development environment",
                "description": "Install Python, FastAPI, and configure IDE",
                "completed": True
            },
            {
                "title": "Design database schema",
                "description": "Create ERD and define table relationships",
                "completed": True
            },
            {
                "title": "Implement CRUD operations",
                "description": "Create endpoints for Create, Read, Update, Delete",
                "completed": True
            },
            {
                "title": "Write unit tests",
                "description": "Add comprehensive test coverage for all endpoints",
                "completed": False
            },
            {
                "title": "Set up CI/CD pipeline",
                "description": "Configure GitHub Actions for automated testing",
                "completed": False
            },
            {
                "title": "Deploy to production",
                "description": "Deploy application to cloud hosting platform",
                "completed": False
            },
            {
                "title": "Add API documentation",
                "description": "Enhance OpenAPI documentation with examples",
                "completed": False
            },
            {
                "title": "Implement authentication",
                "description": "Add JWT-based authentication system",
                "completed": False
            },
        ]

        # Create todos
        created_count = 0
        for todo_data in sample_todos:
            todo = Todo(**todo_data)
            db.add(todo)
            created_count += 1

        db.commit()

        logger.info(f"Successfully seeded {created_count} todos")
        print(f"\n✓ Successfully seeded {created_count} todos")

        # Display summary
        total_count = db.query(Todo).count()
        completed_count = db.query(Todo).filter(Todo.completed == True).count()
        pending_count = total_count - completed_count

        print(f"\nDatabase summary:")
        print(f"  Total todos: {total_count}")
        print(f"  Completed: {completed_count}")
        print(f"  Pending: {pending_count}")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}", exc_info=True)
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_todos()

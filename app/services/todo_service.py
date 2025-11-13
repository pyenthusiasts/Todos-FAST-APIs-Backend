"""Service layer for Todo operations."""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    """Service class for Todo CRUD operations."""

    @staticmethod
    def get_all_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Retrieve all todos from the database.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Todo objects
        """
        return db.query(Todo).offset(skip).limit(limit).all()

    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a todo by its ID.

        Args:
            db: Database session
            todo_id: ID of the todo to retrieve

        Returns:
            Todo object if found, None otherwise
        """
        return db.query(Todo).filter(Todo.id == todo_id).first()

    @staticmethod
    def create_todo(db: Session, todo: TodoCreate) -> Todo:
        """
        Create a new todo.

        Args:
            db: Database session
            todo: TodoCreate schema with todo data

        Returns:
            Created Todo object
        """
        db_todo = Todo(
            title=todo.title,
            description=todo.description,
            completed=todo.completed
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """
        Update an existing todo.

        Args:
            db: Database session
            todo_id: ID of the todo to update
            todo_update: TodoUpdate schema with updated data

        Returns:
            Updated Todo object if found, None otherwise
        """
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            return None

        # Update only provided fields
        update_data = todo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete_todo(db: Session, todo_id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            db: Database session
            todo_id: ID of the todo to delete

        Returns:
            True if deleted, False if not found
        """
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not db_todo:
            return False

        db.delete(db_todo)
        db.commit()
        return True

    @staticmethod
    def get_total_count(db: Session) -> int:
        """
        Get total count of todos.

        Args:
            db: Database session

        Returns:
            Total count of todos
        """
        return db.query(Todo).count()

    @staticmethod
    def get_completed_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Get all completed todos.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of completed Todo objects
        """
        return db.query(Todo).filter(Todo.completed == True).offset(skip).limit(limit).all()

    @staticmethod
    def get_pending_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Get all pending (incomplete) todos.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of pending Todo objects
        """
        return db.query(Todo).filter(Todo.completed == False).offset(skip).limit(limit).all()

"""API routes for Todo operations."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoList,
    MessageResponse
)
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=TodoList, summary="Get all todos")
def get_all_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all todos with pagination.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
        db: Database session

    Returns:
        TodoList with todos and total count
    """
    todos = TodoService.get_all_todos(db, skip=skip, limit=limit)
    total = TodoService.get_total_count(db)
    return TodoList(todos=todos, total=total)


@router.get("/completed", response_model=List[TodoResponse], summary="Get completed todos")
def get_completed_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all completed todos.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of completed todos
    """
    return TodoService.get_completed_todos(db, skip=skip, limit=limit)


@router.get("/pending", response_model=List[TodoResponse], summary="Get pending todos")
def get_pending_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieve all pending (incomplete) todos.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of pending todos
    """
    return TodoService.get_pending_todos(db, skip=skip, limit=limit)


@router.get("/{todo_id}", response_model=TodoResponse, summary="Get todo by ID")
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific todo by ID.

    Args:
        todo_id: ID of the todo to retrieve
        db: Database session

    Returns:
        Todo with the specified ID

    Raises:
        HTTPException: 404 if todo not found
    """
    todo = TodoService.get_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    return todo


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo"
)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new todo.

    Args:
        todo: TodoCreate schema with todo data
        db: Database session

    Returns:
        The newly created todo
    """
    return TodoService.create_todo(db, todo)


@router.put("/{todo_id}", response_model=TodoResponse, summary="Update a todo")
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing todo.

    Args:
        todo_id: ID of the todo to update
        todo_update: TodoUpdate schema with updated data
        db: Database session

    Returns:
        The updated todo

    Raises:
        HTTPException: 404 if todo not found
    """
    updated_todo = TodoService.update_todo(db, todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    return updated_todo


@router.delete("/{todo_id}", response_model=MessageResponse, summary="Delete a todo")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a todo by ID.

    Args:
        todo_id: ID of the todo to delete
        db: Database session

    Returns:
        Confirmation message

    Raises:
        HTTPException: 404 if todo not found
    """
    deleted = TodoService.delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    return MessageResponse(message="Todo deleted successfully")

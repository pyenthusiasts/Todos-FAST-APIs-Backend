"""Pydantic schemas for Todo."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """Base schema for Todo."""

    title: str = Field(..., min_length=1, max_length=255, description="Title of the todo")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the todo")
    completed: bool = Field(default=False, description="Completion status")


class TodoCreate(TodoBase):
    """Schema for creating a new Todo."""

    pass


class TodoUpdate(BaseModel):
    """Schema for updating a Todo."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    """Schema for Todo response."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TodoList(BaseModel):
    """Schema for list of Todos."""

    todos: list[TodoResponse]
    total: int


class MessageResponse(BaseModel):
    """Generic message response schema."""

    message: str

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# FastAPI instance
app = FastAPI()

# In-memory "database"
todos = []

# Pydantic model for Todo
class Todo(BaseModel):
    id: int 
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[datetime] = None

# Helper function to find a todo by id
def find_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API!"}

# Get all todos
@app.get("/todos", response_model=List[Todo])
def get_todos(
    completed: Optional[bool] = None,
    priority: Optional[str] = Query(None, pattern="^(low|medium|high)$"),
    before: Optional[datetime] = None,
    after: Optional[datetime] = None,
    sort: Optional[str] = Query(None, pattern="^(due_date|priority)$")
):
    filtered = todos
    if completed is not None:
        filtered = [t for t in filtered if t.completed == completed]
    if priority:
        filtered = [t for t in filtered if t.priority == priority]
    if before:
        filtered = [t for t in filtered if t.due_date and t.due_date <= before]
    if after:
        filtered = [t for t in filtered if t.due_date and t.due_date >= after]
    if sort:
        if sort == "due_date":
            filtered = sorted(filtered, key=lambda t: t.due_date if t.due_date else datetime.max)
        elif sort == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            filtered = sorted(filtered, key=lambda t: priority_order.get(t.priority or "medium", 1))
    return filtered

# Get a todo by ID
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Create a new todo
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    if find_todo(todo.id):
        raise HTTPException(status_code=400, detail="Todo with this ID already exists")
    todos.append(todo)
    return todo

# Update an existing todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.completed = updated_todo.completed
    todo.priority = updated_todo.priority
    todo.due_date = updated_todo.due_date
    return todo

# Delete a todo
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.remove(todo)
    return {"message": "Todo deleted successfully"}

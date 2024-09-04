from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

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
def get_todos():
    return todos

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
    return todo

# Delete a todo
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.remove(todo)
    return {"message": "Todo deleted successfully"}

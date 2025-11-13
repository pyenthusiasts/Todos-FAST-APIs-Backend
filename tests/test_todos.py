"""Tests for Todo API endpoints."""
import pytest
from fastapi import status


class TestTodoAPI:
    """Test suite for Todo API endpoints."""

    def test_create_todo(self, client):
        """Test creating a new todo."""
        todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "completed": False
        }
        response = client.post("/api/v1/todos", json=todo_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == todo_data["title"]
        assert data["description"] == todo_data["description"]
        assert data["completed"] == todo_data["completed"]
        assert "id" in data
        assert "created_at" in data

    def test_create_todo_minimal(self, client):
        """Test creating a todo with minimal data."""
        todo_data = {"title": "Minimal Todo"}
        response = client.post("/api/v1/todos", json=todo_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == todo_data["title"]
        assert data["completed"] is False

    def test_get_all_todos(self, client):
        """Test retrieving all todos."""
        # Create some todos
        for i in range(3):
            client.post("/api/v1/todos", json={"title": f"Todo {i}"})

        response = client.get("/api/v1/todos")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "todos" in data
        assert "total" in data
        assert len(data["todos"]) == 3
        assert data["total"] == 3

    def test_get_todo_by_id(self, client):
        """Test retrieving a todo by ID."""
        # Create a todo
        create_response = client.post("/api/v1/todos", json={"title": "Test Todo"})
        todo_id = create_response.json()["id"]

        # Get the todo
        response = client.get(f"/api/v1/todos/{todo_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test Todo"

    def test_get_nonexistent_todo(self, client):
        """Test retrieving a todo that doesn't exist."""
        response = client.get("/api/v1/todos/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_todo(self, client):
        """Test updating a todo."""
        # Create a todo
        create_response = client.post("/api/v1/todos", json={"title": "Original Title"})
        todo_id = create_response.json()["id"]

        # Update the todo
        update_data = {"title": "Updated Title", "completed": True}
        response = client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["completed"] is True

    def test_update_partial_todo(self, client):
        """Test partially updating a todo."""
        # Create a todo
        create_response = client.post(
            "/api/v1/todos",
            json={"title": "Original", "description": "Original desc"}
        )
        todo_id = create_response.json()["id"]

        # Update only the completed status
        response = client.put(f"/api/v1/todos/{todo_id}", json={"completed": True})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Original"
        assert data["completed"] is True

    def test_update_nonexistent_todo(self, client):
        """Test updating a todo that doesn't exist."""
        response = client.put("/api/v1/todos/999", json={"title": "Updated"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_todo(self, client):
        """Test deleting a todo."""
        # Create a todo
        create_response = client.post("/api/v1/todos", json={"title": "To Delete"})
        todo_id = create_response.json()["id"]

        # Delete the todo
        response = client.delete(f"/api/v1/todos/{todo_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Todo deleted successfully"

        # Verify it's deleted
        get_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_todo(self, client):
        """Test deleting a todo that doesn't exist."""
        response = client.delete("/api/v1/todos/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_completed_todos(self, client):
        """Test retrieving completed todos."""
        # Create todos
        client.post("/api/v1/todos", json={"title": "Todo 1", "completed": True})
        client.post("/api/v1/todos", json={"title": "Todo 2", "completed": False})
        client.post("/api/v1/todos", json={"title": "Todo 3", "completed": True})

        response = client.get("/api/v1/todos/completed")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert all(todo["completed"] for todo in data)

    def test_get_pending_todos(self, client):
        """Test retrieving pending todos."""
        # Create todos
        client.post("/api/v1/todos", json={"title": "Todo 1", "completed": True})
        client.post("/api/v1/todos", json={"title": "Todo 2", "completed": False})
        client.post("/api/v1/todos", json={"title": "Todo 3", "completed": False})

        response = client.get("/api/v1/todos/pending")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert all(not todo["completed"] for todo in data)

    def test_pagination(self, client):
        """Test pagination of todos."""
        # Create 10 todos
        for i in range(10):
            client.post("/api/v1/todos", json={"title": f"Todo {i}"})

        # Get first page
        response = client.get("/api/v1/todos?skip=0&limit=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["todos"]) == 5
        assert data["total"] == 10

        # Get second page
        response = client.get("/api/v1/todos?skip=5&limit=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["todos"]) == 5

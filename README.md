# Todo Application Backend with FastAPI

This project demonstrates a simple, demo backend REST API for a **Todo Application** built using **FastAPI**, a modern and fast web framework for building APIs with Python. The API supports basic CRUD operations (Create, Read, Update, Delete) to manage a list of todo items.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Examples](#examples)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

This Todo Application provides a RESTful API that allows users to manage their todo items. The API is built using **FastAPI**, which provides high performance, automatic data validation, and interactive API documentation. It includes endpoints to create, retrieve, update, and delete todo items.

## Features

- **FastAPI Framework**: Built using FastAPI, which provides asynchronous support and high performance.
- **CRUD Operations**: Create, Read, Update, and Delete operations for managing todo items.
- **Automatic API Documentation**: Interactive API documentation generated with **Swagger UI** and **ReDoc**.
- **Pydantic Models**: Data validation and serialization using Pydantic models.
- **Error Handling**: Custom error messages for different HTTP status codes.

## Installation

### Prerequisites

- Python 3.7 or higher

### Install Required Packages

1. **Clone the Repository**:

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/todo-app-fastapi.git
   ```

2. **Navigate to the Directory**:

   Go to the project directory:

   ```bash
   cd todo-app-fastapi
   ```

3. **Install Dependencies**:

   Install FastAPI and Uvicorn using pip:

   ```bash
   pip install fastapi uvicorn
   ```

## Usage

1. **Run the Application**:

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```

   The server will start at `http://127.0.0.1:8000/`.

2. **Access API Documentation**:

   FastAPI provides interactive API documentation at:

   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

The following endpoints are available:

### 1. Get All Todos

- **Endpoint**: `GET /todos`
- **Description**: Retrieve all todo items.
- **Response**: A list of all todo items.

### 2. Get Todo by ID

- **Endpoint**: `GET /todos/{todo_id}`
- **Description**: Retrieve a specific todo item by its ID.
- **Response**: The todo item with the specified ID.

### 3. Create a New Todo

- **Endpoint**: `POST /todos`
- **Description**: Create a new todo item.
- **Request Body**:
  ```json
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, Bread, Cheese, Eggs",
    "completed": false
  }
  ```
- **Response**: The newly created todo item.

### 4. Update an Existing Todo

- **Endpoint**: `PUT /todos/{todo_id}`
- **Description**: Update an existing todo item by its ID.
- **Request Body**:
  ```json
  {
    "id": 1,
    "title": "Buy groceries and fruits",
    "description": "Milk, Bread, Cheese, Eggs, Apples",
    "completed": false
  }
  ```
- **Response**: The updated todo item.

### 5. Delete a Todo

- **Endpoint**: `DELETE /todos/{todo_id}`
- **Description**: Delete a specific todo item by its ID.
- **Response**: A confirmation message.

## Examples

### Using cURL

1. **Create a Todo**:

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"id": 1, "title": "Buy groceries", "description": "Milk, Bread, Cheese, Eggs", "completed": false}' http://127.0.0.1:8000/todos
   ```

2. **Get All Todos**:

   ```bash
   curl -X GET http://127.0.0.1:8000/todos
   ```

3. **Get Todo by ID**:

   ```bash
   curl -X GET http://127.0.0.1:8000/todos/1
   ```

4. **Update a Todo**:

   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"id": 1, "title": "Buy groceries and fruits", "description": "Milk, Bread, Cheese, Eggs, Apples", "completed": false}' http://127.0.0.1:8000/todos/1
   ```

5. **Delete a Todo**:

   ```bash
   curl -X DELETE http://127.0.0.1:8000/todos/1
   ```

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please feel free to open an issue or create a pull request.

### Steps to Contribute

1. **Fork the Repository**: Click the 'Fork' button at the top right of this page.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/your-username/todo-app-fastapi.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes**: Make your changes and commit them with a descriptive message.
   ```bash
   git commit -m "Add: feature description"
   ```
5. **Push Changes**: Push your changes to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using the Todo Application Backend with FastAPI! If you have any questions or feedback, feel free to reach out. Happy coding! 📝🚀

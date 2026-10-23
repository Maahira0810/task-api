# Task API

A simple REST API built with Python and FastAPI to manage to-do tasks. This project demonstrates CRUD operations using in-memory storage.

## Features

- Retrieve all tasks.
- Retrieve a task by ID.
- Create a task.
- Update a task's title or completion status.
- Delete a task.
- Validate incoming requests.
- Return appropriate HTTP status codes.
- Explore and test endpoints using Swagger UI.

## Technologies

- Python
- FastAPI
- Uvicorn

## Setup and Installation

Make sure Python is installed.

Install the dependencies:

```bash
python -m pip install fastapi uvicorn
```

## Run the Application

From the project directory, run:

```bash
python -m uvicorn main:app --reload
```

Open the following address in your browser:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/` | Get API information | 200 |
| GET | `/health` | Check API health | 200 |
| GET | `/tasks` | Get all tasks | 200 |
| GET | `/tasks/{task_id}` | Get a task by ID | 200 |
| POST | `/tasks` | Create a task | 201 |
| PUT | `/tasks/{task_id}` | Update a task | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |

Invalid requests may return `400 Bad Request` or `404 Not Found`.

## Example Requests

### Create a task

```json
{
  "title": "Learn FastAPI"
}
```

### Update a task

```json
{
  "title": "Finish my CRUD API",
  "done": true
}
```

## Storage

Tasks are stored in memory. Data resets when the server restarts. No database is required.

## Interactive Documentation

FastAPI provides interactive API documentation through Swagger UI at `/docs`.

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response
from typing import Any

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple To-do API with CRUD operations."
)

# In-memory storage. Tasks reset when the server restarts.
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Publish project on GitHub", "done": False},
]


def find_task(task_id: int):
    """Return a task by ID, or None if it does not exist."""
    return next(
        (task for task in tasks if task["id"] == task_id),
        None
    )


def validate_title(title: Any):
    """Return an error response if the title is invalid."""
    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )
    return None


@app.get("/", description="Get API information.")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", description="Check whether the API is running.")
def health():
    return {"status": "ok"}


@app.get("/tasks", description="Get all tasks.")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", description="Get a task by ID.")
def get_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    return task


@app.post(
    "/tasks",
    status_code=201,
    description="Create a task."
)
def create_task(body: dict = Body(...)):
    # Validate the request body.
    if not isinstance(body, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"}
        )

    error = validate_title(body.get("title"))
    if error:
        return error

    # Assign the next available ID.
    next_id = max(
        (task["id"] for task in tasks),
        default=0
    ) + 1

    new_task = {
        "id": next_id,
        "title": body["title"].strip(),
        "done": False
    }

    tasks.append(new_task)
    return new_task


@app.put(
    "/tasks/{task_id}",
    description="Update a task by ID."
)
def update_task(task_id: int, body: dict = Body(...)):
    # Check whether the task exists.
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    # Reject an empty body.
    if not body:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    # Only title and done can be updated.
    allowed_fields = {"title", "done"}

    if not all(key in allowed_fields for key in body):
        return JSONResponse(
            status_code=400,
            content={"error": "Only title and done can be updated"}
        )

    # Validate title if supplied.
    if "title" in body:
        error = validate_title(body["title"])
        if error:
            return error

    # Validate done if supplied.
    if "done" in body and type(body["done"]) is not bool:
        return JSONResponse(
            status_code=400,
            content={"error": "Done must be true or false"}
        )

    # Apply the changes.
    if "title" in body:
        task["title"] = body["title"].strip()

    if "done" in body:
        task["done"] = body["done"]

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    description="Delete a task by ID."
)
def delete_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )

    tasks.remove(task)

    # HTTP 204 responses must have no body.
    return Response(status_code=204)

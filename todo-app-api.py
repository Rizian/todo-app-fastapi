from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    title: str
    desc: str = "no description"
    completed: bool = False

class UpdateTodo(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None
    completed: Optional[bool] = None

todos_db = {
    1: Todo(title="test", desc="This is just a test", completed=False)
}


@app.get("/")
async def index():
    return {"message": "This is a to-do list API"}

@app.get("/get-todos/")
async def get_todos():
    return todos_db

@app.get("/get-todo/{id}")
async def get_todo(id: int):
    if id not in todos_db:
        return {"error": "id doesn't exist"}
    return todos_db[id]

@app.post("/create-todo/{id}")
async def create_todo(id: int, todo: Todo):
    if id in todos_db:
        return {"error": "id already exists, cannot overwrite"}
    todos_db[id] = todo
    return todos_db[id]

@app.put("/update-todo/{id}")
async def update_todo(id: int, student: UpdateTodo):
    if id not in todos_db:
        return {"error": "id doesn't exist"}
    
    if student.title != None:
        todos_db[id].title = student.title

    if student.desc != None:
        todos_db[id].desc = student.desc

    if student.completed != None:
        todos_db[id].completed = student.completed

    return todos_db[id]

@app.delete("/delete-todo/{id}")
async def delete_todo(id: int):
    if id not in todos_db:
        return {"error": "id doesn't exist"}
    del todos_db[id]
    return {"message": "item has been deleted successfully"}
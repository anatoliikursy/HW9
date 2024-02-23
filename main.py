from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    text: str

tasks = [
    {"id": 1, "title": "Приклад задачі 1", "text": "Опис першої задачі"},
    {"id": 2, "title": "Приклад задачі 2", "text": "Опис другої задачі"},
]

@app.get("/")
def read_root():
    return {"message": "Welcome to my API"}
  
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="задачу не знайдено")

@app.post("/create_task", status_code=201)
def create_task(task: Task):
    if any(t["id"] == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="id задачі вже існує")
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for id, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[id] = updated_task
            return {"message": f"Task з id {task_id} замінено"}
    raise HTTPException(status_code=404, detail="задачу не знайдено")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": f"Задачу з id {task_id} успішно видалено"}
    raise HTTPException(status_code=404, detail="Задачу не знайдено")


#unvicorn main:app --reload
from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

import models
models.Base.metadata.create_all(bind=engine)

app=FastAPI(
    title= "ToDo List API",
    description= "A simple ToDo List API built with FastAPI and SQLAlchemy",
    version= "1.0.0"
)

@app.get("/")
def root():
    return {"message": "ToDoAPI is running"}

@app.post(
    "/tasks/", 
    response_model=TaskResponse, 
    status_code=201
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    new_Task = Task(
        title= task_data.title,
        description= task_data.description,
        completed= task_data.completed
    )
    db.add(new_Task)

    db.commit()

    db.refresh(new_Task)

    return new_Task

@app.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()
    return tasks

@app.get("/task/{task_id}", response_model=TaskResponse)
def get_task(
    task_id:int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id:int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed

    db.commit()

    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
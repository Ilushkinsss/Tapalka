from fastapi import FastAPI, HTTPException
from typing import List
from models import user, task, referral, CompletedTask
from db import database

app = FastAPI()
db = database(db_name='postgres', user='postgres', password='861211955233iK')

# Пользователи

@app.post("/users/", response_model=user)
def create_user(user: user):
    query = "INSERT INTO users (telegram_id) VALUES ($1) RETURNING id;"
    user_id = db.execute(query, (user.telegram_id,))
    user.id = user_id
    return user

@app.get("/users/", response_model=List[user])
def get_users():
    query = "SELECT * FROM users;"
    users = db.fetch_all(query)
    return []

@app.get("/users/{user_id}", response_model=user)
def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = $1;"
    user = db.fetch_one(query, (user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=user)
def update_user(user_id: int, user: user):
    query = "UPDATE users SET telegram_id = $1 WHERE id = $2 RETURNING *;"
    updated_user = db.fetch_one(query, (user.telegram_id, user_id))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = $1;"
    result = db.execute(query, (user_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Задания

@app.post("/tasks/", response_model=task)
def create_task(task: task):
    query = "INSERT INTO tasks (task_name, task_points) VALUES ($1, $2) RETURNING id;"
    task_id = db.execute(query, (task.task_name, task.task_points))
    task.id = task_id
    return task

@app.get("/tasks/", response_model=List[task])
def get_tasks():
    query = "SELECT * FROM tasks;"
    tasks = db.fetch_all(query)
    return []

@app.get("/tasks/{task_id}", response_model=task)
def get_task(task_id: int):
    query = "SELECT * FROM tasks WHERE id = $1;"
    task = db.fetch_one(query, (task_id,))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=task)
def update_task(task_id: int, task: task):
    query = "UPDATE tasks SET task_name = $1, task_points = $2 WHERE id = $3 RETURNING *;"
    updated_task = db.fetch_one(query, (task.task_name, task.task_points, task_id))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE id = $1;"
    result = db.execute(query, (task_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

# Рефералы

@app.post("/referrals/", response_model=referral)
def create_referral(referral: referral):
    query = "INSERT INTO referrals (user_id, referred_user_id) VALUES ($1, $2) RETURNING id;"
    referral_id = db.execute(query, (referral.user_id, referral.referred_user_id))
    referral.id = referral_id
    return referral

@app.get("/referrals/")
def get_referrals():
    query = "SELECT * FROM referrals;"
    referrals = db.fetch_all(query)
    return []

# Завершенные задания

completed_tasks_db = []  # Временное хранилище для завершенных заданий

@app.post("/completed_tasks/", response_model=CompletedTask)
def create_completed_task(completed_task: CompletedTask):
    completed_tasks_db.append(completed_task)
    return completed_task

@app.get("/completed_tasks/", response_model=List[CompletedTask])
def get_completed_tasks():
    return completed_tasks_db

@app.get("/completed_tasks/{user_id}", response_model=List[CompletedTask])
def get_completed_tasks_by_user(user_id: int):
    user_completed_tasks = [task for task in completed_tasks_db if task.user_id == user_id]
    return user_completed_tasks

@app.delete("/completed_tasks/{task_id}")
def delete_completed_task(task_id: int):
    global completed_tasks_db
    completed_tasks_db = [task for task in completed_tasks_db if task.task_id != task_id]
    return {"message": "Completed task deleted successfully"}

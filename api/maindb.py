from fastapi import FastAPI, HTTPException
from typing import List
from db.models import User, CompletedTask, Referral, Task
from db.Database import Database

app = FastAPI()
db = Database(db_name='postgres', user='postgres', password='861211955233iK')

# Пользователи
@app.post("/users/", response_model=User)
def create_user(user: User):
    query = "SELECT id FROM users WHERE telegram_id = $1;"
    existing_user = db.fetch_one(query, (user.telegram_id,))
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this telegram_id already exists")

    query = "INSERT INTO users (telegram_id) VALUES ($1) RETURNING id;"
    user_id = db.execute(query, (user.telegram_id,))
    user.id = user_id
    return user

@app.get("/users/", response_model=List[User])
def get_users():
    query = "SELECT * FROM users;"
    users = db.fetch_all(query)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = $1;"
    user = db.fetch_one(query, (user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
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
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    query = "INSERT INTO tasks (task_name, task_points) VALUES ($1, $2) RETURNING id;"
    task_id = db.execute(query, (task.task_name, task.task_points))
    if not task_id:
        raise HTTPException(status_code=400, detail="Failed to create task")
    task.id = task_id
    return task

@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    query = "SELECT * FROM tasks;"
    tasks = db.fetch_all(query)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    query = "SELECT * FROM tasks WHERE id = $1;"
    task = db.fetch_one(query, (task_id,))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
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
@app.post("/referrals/", response_model=Referral)
def create_referral(referral: Referral):
    query = "SELECT * FROM referrals WHERE user_id = $1 AND referred_user_id = $2;"
    existing_referral = db.fetch_one(query, (referral.user_id, referral.referred_user_id))
    if existing_referral:
        raise HTTPException(status_code=400, detail="Referral already exists")

    query = "INSERT INTO referrals (user_id, referred_user_id) VALUES ($1, $2) RETURNING id;"
    referral_id = db.execute(query, (referral.user_id, referral.referred_user_id))
    referral.id = referral_id
    return referral

@app.get("/referrals/")
def get_referrals():
    query = "SELECT * FROM referrals;"
    referrals = db.fetch_all(query)
    if not referrals:
        raise HTTPException(status_code=404, detail="No referrals found")
    return referrals

# Завершенные задания
@app.post("/completed_tasks/", response_model=CompletedTask)
def create_completed_task(completed_task: CompletedTask):
    query = "INSERT INTO completed_tasks (user_id, task_id, completed_at) VALUES ($1, $2, NOW()) RETURNING id;"
    task_id = db.execute(query, (completed_task.user_id, completed_task.task_id))
    completed_task.id = task_id
    return completed_task

@app.get("/completed_tasks/", response_model=List[CompletedTask])
def get_completed_tasks():
    query = "SELECT * FROM completed_tasks;"
    completed_tasks = db.fetch_all(query)
    if not completed_tasks:
        raise HTTPException(status_code=404, detail="No completed tasks found")
    return completed_tasks

@app.get("/completed_tasks/{user_id}", response_model=List[CompletedTask])
def get_completed_tasks_by_user(user_id: int):
    query = "SELECT * FROM completed_tasks WHERE user_id = $1;"
    completed_tasks = db.fetch_all(query, (user_id,))
    if not completed_tasks:
        raise HTTPException(status_code=404, detail="No completed tasks found for this user")
    return completed_tasks

@app.delete("/completed_tasks/{task_id}")
def delete_completed_task(task_id: int):
    query = "DELETE FROM completed_tasks WHERE task_id = $1;"
    result = db.execute(query, (task_id,))
    if result == 0:
        raise HTTPException(status_code=404, detail="Completed task not found")
    return {"message": "Completed task deleted successfully"}

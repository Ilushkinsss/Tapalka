from fastapi import FastAPI, HTTPException
from databases import Database
from api.models.UserAPI import UserCreate, UserResponse
from api.models.ReferralAPI import ReferralCreate, ReferralResponse
from api.models.TaskAPI import TaskCreate, TaskResponse
from api.models.CompletedTaskAPI import CompletedTaskCreate, CompletedTaskResponse

DATABASE_URL = "postgresql://postgres:861211955233iK@localhost/postgres"
db = Database(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    query = """
        INSERT INTO users (telegram_id, total_points, total_referrals, total_tasks, company, lvl_points)
        VALUES (:telegram_id, :total_points, :total_referrals, :total_tasks, :company, :lvl_points)
        RETURNING id;
    """
    user_id = await db.execute(query, values={
        "telegram_id": user.telegram_id,
        "total_points": user.total_points,
        "total_referrals": user.total_referrals,
        "total_tasks": user.total_tasks,
        "company": user.company,
        "lvl_points": user.lvl_points,
    })
    return {
        "id": user_id,
        "telegram_id": user.telegram_id,
        "total_points": user.total_points,
        "total_referrals": user.total_referrals,
        "total_tasks": user.total_tasks,
        "company": user.company,
        "lvl_points": user.lvl_points,
    }


@app.post("/referrals/", response_model=ReferralResponse)
async def create_referral(referral: ReferralCreate):
    # Проверка, существует ли уже такой реферал
    query = """
        SELECT id FROM referrals
        WHERE user_request_telegram_id = :user_request_telegram_id 
        AND user_invited_telegram_id = :user_invited_telegram_id;
    """
    existing_referral = await db.fetch_one(query, values={
        "user_request_telegram_id": referral.user_request_telegram_id,
        "user_invited_telegram_id": referral.user_invited_telegram_id
    })
    if existing_referral:
        raise HTTPException(status_code=400, detail="Referral already exists")

    # Создание нового реферала
    query = """
        INSERT INTO referrals (user_request_telegram_id, user_invited_telegram_id)
        VALUES (:user_request_telegram_id, :user_invited_telegram_id) 
        RETURNING id;
    """
    referral_id = await db.execute(query, values={
        "user_request_telegram_id": referral.user_request_telegram_id,
        "user_invited_telegram_id": referral.user_invited_telegram_id
    })
    return {
        "id": referral_id,
        "user_request_telegram_id": referral.user_request_telegram_id,
        "user_invited_telegram_id": referral.user_invited_telegram_id,
    }

@app.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    query = """
        INSERT INTO tasks (task_name, task_description, task_points, task_url)
        VALUES (:task_name, :task_description, :task_points, :task_url)
        RETURNING id;
    """
    task_id = await db.execute(query, values={
        "task_name": task.task_name,
        "task_description": task.task_description,
        "task_points": task.task_points,
        "task_url": task.task_url,
    })
    return {
        "id": task_id,
        "task_name": task.task_name,
        "task_description": task.task_description,
        "task_points": task.task_points,
        "task_url": task.task_url,
    }


@app.post("/completed_tasks/", response_model=CompletedTaskResponse)
async def create_completed_task(completed_task: CompletedTaskCreate):
    query = """
        INSERT INTO completed_tasks (user_id, task_id)
        VALUES (:user_id, :task_id)
        RETURNING id;
    """
    completed_task_id = await db.execute(query, values={
        "user_id": completed_task.user_id,
        "task_id": completed_task.task_id,
    })
    return {
        "id": completed_task_id,
        "user_id": completed_task.user_id,
        "task_id": completed_task.task_id,
    }

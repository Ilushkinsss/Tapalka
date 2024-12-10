from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    task_name: str
    task_description: str
    task_points: int
    task_url: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True

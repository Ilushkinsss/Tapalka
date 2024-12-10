from pydantic import BaseModel

class CompletedTaskBase(BaseModel):
    user_id: int
    task_id: int

class CompletedTaskCreate(CompletedTaskBase):
    pass

class CompletedTaskResponse(CompletedTaskBase):
    id: int

    class Config:
        orm_mode = True

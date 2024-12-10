from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    telegram_id: int
    total_points: Optional[int] = 0
    total_referrals: Optional[int] = 0
    total_tasks: Optional[int] = 0
    company: Optional[str] = None
    lvl_points: Optional[int] = 0

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

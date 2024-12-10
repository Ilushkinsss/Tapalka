from pydantic import BaseModel

class ReferralBase(BaseModel):
    user_request_telegram_id: int
    user_invited_telegram_id: int

class ReferralCreate(ReferralBase):
    pass

class ReferralResponse(ReferralBase):
    id: int

    class Config:
        orm_mode = True

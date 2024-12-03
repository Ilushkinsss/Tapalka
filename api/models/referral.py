from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Referral(Base):
    __tablename__ = 'referrals'

    id = Column(Integer, primary_key=True)
    user_request_telegram_id = Column(Integer, nullable=False)
    user_invited_telegram_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Referral(id={self.id}, user_request_telegram_id={self.user_request_telegram_id}, user_invited_telegram_id={self.user_invited_telegram_id})>"

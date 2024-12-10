from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    total_points = Column(Integer, default=0)
    total_referrals = Column(Integer, default=0)
    total_tasks = Column(Integer, default=0)
    company = Column(String(255), nullable=True)  # Сделано nullable=True для опциональности
    lvl_points = Column(Integer, default=0)

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"telegram_id={self.telegram_id}, "
            f"total_points={self.total_points}, "
            f"total_referrals={self.total_referrals}, "
            f"total_tasks={self.total_tasks}, "
            f"company={self.company}, "
            f"lvl_points={self.lvl_points})>"
        )


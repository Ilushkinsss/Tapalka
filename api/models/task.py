from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    task_points = Column(Integer, nullable=False)
    task_description = Column(String)
    task_url = Column(String(255))

    def __repr__(self):
        return f"<Task(id={self.id}, task_name={self.task_name}, task_points={self.task_points})>"

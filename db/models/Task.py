from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(255), nullable=False)
    task_points = Column(Integer, nullable=False)
    task_description = Column(String, nullable=True)
    task_url = Column(String(255), nullable=True)

    def __repr__(self):
        return (
            f"<Task(id={self.id}, "
            f"task_name={self.task_name}, "
            f"task_points={self.task_points}, "
            f"task_description={self.task_description}, "
            f"task_url={self.task_url})>"
        )


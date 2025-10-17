from sqlalchemy import *
from sqlalchemy.sql import *
from database import Base
from sqlalchemy.orm import *

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index = True, nullable = False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tags = Column(JSON, nullable=True)
    meta = Column(JSON, nullable=True)
    #user = relationship("User", back_populates="posts", uselist=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique = True, nullable = False)
    meta = Column(JSON, nullable=True)
    #posts = relationship("Task", back_populates= "user", uselist=True)

from sqlalchemy import *
from sqlalchemy.sql import func
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index = True, nullable = False)
    description = Column(String)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    tags = Column(JSON, nullable=True)
    meta = Column(JSON, nullable=True)





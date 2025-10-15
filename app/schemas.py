from pydantic import BaseModel
from typing import *
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    meta: Optional[dict[str, Any]] = None

# ����� ��� �������� �����
class TaskCreate(TaskBase):
    pass

# ����� ��� ������ API
class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True



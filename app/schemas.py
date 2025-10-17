from pydantic import BaseModel
from typing import *
from datetime import datetime
from models import *

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    meta: Optional[dict[str, Any]] = None
    #owner_id: Optional[int] = None
    #owner: Optional[User] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    user_name: str
    meta: Optional[dict[str, Any]] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    user_name: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
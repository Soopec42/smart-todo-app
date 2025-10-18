from pydantic import BaseModel, field_validator
from typing import *
from datetime import datetime
from models import *

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    meta: Optional[dict[str, Any]] = None
    
    @field_validator('title')
    @classmethod
    def validate_title_not_empty_or_whitespace(cls, v):
        stripped = v.strip()
        if not stripped:  
            raise ValueError('Title cannot be empty or consist only of whitespace')
        if len(stripped) < 2:  
            raise ValueError('Title must be at least 2 characters long')
        if len(stripped) > 200: 
            raise ValueError('Title cannot exceed 200 characters')
        return stripped  




class TaskCreate(TaskBase):
    owner_id: Optional[int] = None
    owner: Optional[User] = None

class TaskUpdate(TaskBase):
    owner_id: Optional[int] = None
    owner: Optional[User] = None
    title: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    owner_id: Optional[int] = None
    owner: Optional[User] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    user_name: str
    meta: Optional[dict[str, Any]] = None

    @field_validator('user_name')
    @classmethod
    def validate_title_not_empty_or_whitespace(cls, v):
        stripped = v.strip()
        if not stripped:  
            raise ValueError('Title cannot be empty or consist only of whitespace')
        if len(stripped) < 2:  
            raise ValueError('Title must be at least 2 characters long')
        if len(stripped) > 200: 
            raise ValueError('Title cannot exceed 200 characters')
        return stripped  

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    user_name: Optional[str] = None

class User(UserBase):
    id: int
    tasks: List[Task] = []

    class Config:
        from_attributes = True
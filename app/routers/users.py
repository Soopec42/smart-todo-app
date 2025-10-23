from fastapi import *
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession

import models, schemas, crud
from database import get_db

router = APIRouter()

@router.post("/", response_model = schemas.User)
async def create_new_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db = db, user = user)

@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db = db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model = List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(skip = skip, limit = limit, db = db)
    return users

@router.patch("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.TaskUpdate, db = Depends(get_db)):
    db_user = await crud.update_user(db = db, user_id = user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
async def delete_existing_user(user_id = int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_user(db = db, user_id = user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.patch("/{user_id}/assign/{task_id}", response_model = schemas.Task)
async def task_to_user(task_id: int, user_id: int, db: AsyncSession = Depends(get_db)): 
    db_task = await crud.assign_task_to_user(db, task_id=task_id, user_id=user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("/{user_id}/tasks/batch", response_model=List[schemas.Task])
async def assign_tasks_to_user_batch(user_id: int, task_ids: List[int], db: AsyncSession = Depends(get_db)):
    db_tasks = await crud.assign_tasks_to_user(db, task_ids=task_ids, user_id=user_id)
    if db_tasks is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_tasks

@router.post("/{user_id}/tasks", response_model=schemas.Task)
async def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.create_task_and_assign(task = task, user_id = user_id, db = db)
    return db_task







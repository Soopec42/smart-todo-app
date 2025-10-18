from ast import List
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from types import *
import models
import schemas

async def create_task(db: AsyncSession, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    return result.scalar_one_or_none()

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Task).offset(skip).limit(limit))
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskUpdate):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    db_task = result.scalar_one_or_none()
    
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    
    return db_task

async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    db_task = result.scalar_one()
    
    if db_task:
        await db.delete(db_task)
        await db.commit()
        return True
    return False

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(user_id == models.User.id))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 0):
    result = db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalar().all()

async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate):
    result = await db.execute(select(models.User).where(user_id == models.User.id))
    db_user = result.scalar_one_or_none()
    
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)

    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(user_id == models.User.id))
    db_user = result.scalar_one_or_none()

    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

async def assign_task_to_user(db: AsyncSession, task_id: int, user_id: int):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    db_task = result.scalar_one_or_none()

    if db_task is None:
        return None

    us_result = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = us_result.scalar_one_or_none()

    if db_user is None:
        return None

    db_task.owner = db_user
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def assign_tasks_to_user(db: AsyncSession, task_ids: List[int], user_id: int):
    result = await db.execute(select(models.Task).where(models.Task.id.in_(task_ids)))
    db_tasks = result.scalars().all()

    if db_tasks is None:
        return None

    us_result = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = us_result.scalar_one_or_none()

    if db_user is None:
        return None

    for task in db_tasks:
        task.owner = db_user
    await db.commit()
    for task in db_tasks:
        await db.refresh(task)
    return db_tasks

async def create_task_and_assign(db: AsyncSession, task: schemas.TaskCreate, user_id: int):

    us_result = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = us_result.scalar_one_or_none()

    if db_user is None:
        return None

    db_task = models.Task(**task.dict(), owner_id=user_id, owner = db_user)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task








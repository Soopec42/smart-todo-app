from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
    db_task = result.scalar_one_or_none()
    
    if db_task:
        await db.delete(db_task)
        await db.commit()
        return True
    return False
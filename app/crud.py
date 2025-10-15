from sqlalchemy.ext.asyncio import *
from sqlalchemy import select
from typing import List, Optional
import models
import schemas

async def create_task(db: AsyncSession, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(
        title = task.title,
        description = task.description,
        tags = task.tags,
        meta = task.meta)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Task]:
    result = await db.execute(select(models.Task).offset(skip).limit(int))
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: int) -> Optional[models.Task]:
    result = await db.execute(select(models.Task).where(task_id == models.Task.id))
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskCreate) -> Optional[models.Task]:
    db_task = await get_task(db, task_id)
    if db_task:
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    db_task = await get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False



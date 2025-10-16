from fastapi import *
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
import crud
from database import *

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app = FastAPI(title="Smart Todo App", version='1.0.0')


@app.on_event("startup")
async def on_startup():
    await create_tables()

@app.post("/tasks/", response_model=schemas.Task)
async def create_new_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db = db, task = task)

@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await crud.get_task(db = db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/tasks/", response_model=List[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    tasks = await crud.get_tasks(skip = skip, limit = limit, db = db)
    return tasks

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_existing_task(task_id: int, task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.update_task(db = db, task_id = task_id, task_update= task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}





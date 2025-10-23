from fastapi import *
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
import models
import crud
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Task)
async def create_new_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db = db, task = task)

@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await crud.get_task(db = db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/", response_model=List[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    tasks = await crud.get_tasks(skip = skip, limit = limit, db = db)
    return tasks

@router.patch("/{task_id}", response_model=schemas.Task)
async def update_existing_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.update_task(db = db, task_id = task_id, task_update= task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.get("/search/", response_model=List[schemas.Task])
async def search_tasks(
    q: str,
    search_in: List[str] =Query(["title", "description"]),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    search_query = schemas.SearchQuery(q=q, search_in=search_in, skip=skip, limit=limit)
    tasks = await crud.advanced_search_tasks(
        db=db,
        search_query=search_query
    )
    return tasks





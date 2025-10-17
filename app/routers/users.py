from fastapi import *
from typing import *
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas, crud
from ..database import *

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

@router.ger("/", response_model = List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(skip = skip, limit = limit, db = db)
    return users

@router.put("/{user_id}", response_model=schemas.User)
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



from fastapi import *
import models
from routers import tasks, users  
import crud, schemas    
from database import engine, get_db

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)

app = FastAPI(title="Smart Todo App", version='1.0.0')


@app.on_event("startup")
async def on_startup():
    await delete_tables()
    await create_tables()

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/users", tags=["users"])




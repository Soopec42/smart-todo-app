from fastapi import *
from .routers import tasks, users

import models, schemas, crud
from database import *

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app = FastAPI(title="Smart Todo App", version='1.0.0')


@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/users", tags=["users"])




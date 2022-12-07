"""App start file."""

from fastapi import FastAPI

from db import models
from db.database import engine
from routers import bills, dishes, waiters

app = FastAPI()
app.include_router(waiters.router)
app.include_router(dishes.router)
app.include_router(bills.router)

models.Base.metadata.create_all(bind=engine)


@app.get("/", description="Check health server status.", tags=["API status"])
async def root():
    return {"message": "Server is OK"}

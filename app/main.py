"""App start file."""

from fastapi import FastAPI

from app.db import models
from app.db.database import engine
from app.routers import bills, dishes, root, waiters

app = FastAPI(title="Restaurant API")

app.include_router(waiters.router)
app.include_router(dishes.router)
app.include_router(bills.router)
app.include_router(root.router)

models.Base.metadata.create_all(bind=engine)

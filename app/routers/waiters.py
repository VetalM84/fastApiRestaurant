"""GET endpoints for waiter."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_waiter
from app.db.database import get_db
from app.schemas import WaiterBase, WaiterOut, WaiterIn

router = APIRouter(prefix="/waiters", tags=["waiters"])


@router.get("/", response_model=list[WaiterBase])
async def get_all_waiters(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all waiters."""
    items = crud_waiter.get_all_waiters(db, skip=skip, limit=limit)
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="Waiters not found")
    return items


@router.get("/{waiter_id}", response_model=WaiterOut, status_code=status.HTTP_200_OK)
async def get_waiter(waiter_id: int, db: Session = Depends(get_db)):
    """Get a waiter by id with a list of the bills."""
    db_waiter = crud_waiter.get_waiter(db, waiter_id=waiter_id)
    if not db_waiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Waiter not found"
        )
    return db_waiter


@router.post("/", response_model=WaiterOut, status_code=status.HTTP_201_CREATED)
async def create_waiter(waiter: WaiterIn, db: Session = Depends(get_db)):
    """Get a waiter by id with a list of the bills."""
    new_waiter = crud_waiter.create_waiter(db, waiter=waiter)
    return new_waiter

"""GET endpoints for users."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import WaiterBase, WaiterOut, BillIn, DishIn, BillBase, DishBase
from db import crud
from db.database import get_db

router = APIRouter(prefix="/waiters", tags=["waiters"])


@router.get("/", response_model=list[WaiterBase])
async def get_all_waiters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all waiters."""
    items = crud.get_all_waiters(db, skip=skip, limit=limit)
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="Waiters not found")
    return items


@router.get("/{waiter_id}", response_model=WaiterOut, status_code=status.HTTP_200_OK)
async def get_waiter(waiter_id: int, db: Session = Depends(get_db)):
    """Get a waiter by id with a list of the bills."""
    db_waiter = crud.get_waiter(db, waiter_id=waiter_id)
    if not db_waiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Waiter not found"
        )
    return db_waiter

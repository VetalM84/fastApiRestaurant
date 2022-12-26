"""Endpoints for waiter."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_waiter
from app.crud.dependencies import JWTBearer, get_current_user
from app.db.database import get_db
from app.db.models import Waiter
from app.schemas import WaiterBase, WaiterIn, WaiterOut

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
async def get_waiter(
    waiter_id: int,
    db: Session = Depends(get_db),
    logged_in_waiter: Waiter = Depends(get_current_user),
):
    """Get a waiter by id with a list of the bills."""
    if waiter_id != logged_in_waiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't view this waiter."
        )
    db_waiter = crud_waiter.get_waiter(db, waiter_id=waiter_id)
    if not db_waiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Waiter not found"
        )
    return db_waiter


@router.post(
    "/", response_model=WaiterOut, status_code=status.HTTP_201_CREATED, tags=["auth"]
)
async def create_waiter(waiter: WaiterIn, db: Session = Depends(get_db)):
    """Create a waiter."""
    new_waiter = crud_waiter.create_waiter(db, waiter=waiter)
    return new_waiter


@router.get("/me", response_model=WaiterBase)
async def get_logged_in_waiter(current_user: Waiter = Depends(get_current_user)):
    """Get current logged in user."""
    return current_user

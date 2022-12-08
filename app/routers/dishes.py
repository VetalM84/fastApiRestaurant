"""Endpoints for dish."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_bill
from app.db.database import get_db
from app.schemas import DishBase, DishIn

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.get("/{dish_id}", response_model=DishBase, status_code=status.HTTP_200_OK)
async def get_dish(dish_id: int, db: Session = Depends(get_db)):
    """Get a dish by id."""
    db_dish = crud_bill.get_bill(db, bill_id=dish_id)
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found",
        )
    return db_dish

"""Endpoints for dish."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_dish
from app.crud.dependencies import get_current_user
from app.db.database import get_db
from app.schemas import DishBase, DishIn

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.get("/{dish_id}", response_model=DishBase, status_code=status.HTTP_200_OK)
async def get_dish(dish_id: int, db: Session = Depends(get_db)):
    """Get a dish by id."""
    db_dish = crud_dish.get_dish(db, dish_id=dish_id)
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found",
        )
    return db_dish


@router.post(
    "/",
    response_model=DishBase,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def create_dish(dish: DishIn, db: Session = Depends(get_db)):
    """Create a new dish."""
    return crud_dish.create_dish(db=db, dish=dish)


@router.get("/", response_model=list[DishBase])
async def get_all_dishes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all dishes."""
    dishes = crud_dish.get_all_dishes(db, skip=skip, limit=limit)
    if len(dishes) == 0:
        raise HTTPException(status_code=404, detail="Dishes not found")
    return dishes


@router.delete(
    "/{dish_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    """Delete a dish by id."""
    db_dish = crud_dish.get_dish(db, dish_id=dish_id)
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found",
        )
    return crud_dish.delete_dish(db=db, dish_id=dish_id)

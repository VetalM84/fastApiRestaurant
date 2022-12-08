"""Functions to create, read, update, and delete data from the database."""

from fastapi import HTTPException, status
from schemas import BillBase, BillIn, DishBase, DishIn, WaiterBase, WaiterOut
from sqlalchemy.orm import Session

from db.models import Bill, Dish, Waiter


def get_waiter(db: Session, waiter_id: int):
    """Get a waiter by id."""
    db_waiter = db.query(Waiter).filter(Waiter.id == waiter_id).first()
    return db_waiter


def get_all_waiters(db: Session, skip: int = 0, limit: int = 100):
    """Get all waiters."""
    db_waiters = db.query(Waiter).offset(skip).limit(limit).all()
    return db_waiters


def tip(amount, bill):
    """Calculate tips."""
    if bill.tip_included:
        return round(amount * bill.tip_percent / 100, 2)
    return 0.00


def create_bill(db: Session, bill: BillIn):
    """Create a new bill."""
    dishes_list, cost_list = [], []
    for dish_id in bill.dishes:
        try:
            dish = get_dish(db, dish_id=dish_id)
            dishes_list.append(dish)
            cost_list.append(dish.cost)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dish id {dish_id} not found",
            )
    bill.dishes = dishes_list
    print(bill.dishes)
    amount = round(sum(cost_list), 2)
    bill.amount = amount + tip(amount=amount, bill=bill)

    new_bill = Bill(**bill.dict())

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill


def get_bill(db: Session, bill_id: int):
    """Get a bill by id."""
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()
    return db_bill


def get_dish(db: Session, dish_id: int):
    """Get a dish by id."""
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    return db_dish


def get_all_dishes(db: Session, skip: int = 0, limit: int = 100):
    """Get all dishes."""
    db_dishes = db.query(Dish).offset(skip).limit(limit).all()
    return db_dishes

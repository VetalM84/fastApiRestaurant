"""CRUD functions for DB operations with bill."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.crud_dish import get_dish
from app.db.models import Bill
from app.schemas import BillIn


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

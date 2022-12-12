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
    dishes_objects_list, dishes_cost_list = [], []
    for dish_id in bill.dishes:
        try:
            dish = get_dish(db, dish_id=dish_id)
            # retrieve a dish object from given id and append it to list
            dishes_objects_list.append(dish)
            # assign new attr to dish object equal to ordered dishes count
            dish.count = bill.dishes.count(dish_id)
            # retrieve a dish cost from given id and append it to list
            dishes_cost_list.append(dish.cost)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dish id {dish_id} not found",
            )
    # update list of id's with a list of appropriate objects
    bill.dishes = dishes_objects_list

    amount = round(sum(dishes_cost_list), 2)
    # add tip to total amount of bill
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


def delete_bill(db: Session, bill_id: int):
    """Delete a bill by id."""
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()
    db.delete(db_bill)
    db.commit()
    return db_bill

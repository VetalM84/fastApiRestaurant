"""CRUD functions for DB operations with dish."""

from sqlalchemy.orm import Session

from app.db.models import Dish
from app.schemas import DishIn


def get_dish(db: Session, dish_id: int):
    """Get a dish by id."""
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    return db_dish


def get_all_dishes(db: Session, skip: int = 0, limit: int = 100):
    """Get all dishes."""
    db_dishes = db.query(Dish).offset(skip).limit(limit).all()
    return db_dishes


def create_dish(db: Session, dish: DishIn):
    """Create a new dish."""
    new_dish = Dish(
        name=dish.name,
        description=dish.description,
        image_url=dish.image_url,
        cost=dish.cost,
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


def delete_dish(db: Session, dish_id: int):
    """Delete a dish by id."""
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    db.delete(db_dish)
    db.commit()
    return db_dish

"""CRUD functions for DB operations with dish."""

from sqlalchemy.orm import Session

from app.db.models import Dish


def get_dish(db: Session, dish_id: int):
    """Get a dish by id."""
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    return db_dish


def get_all_dishes(db: Session, skip: int = 0, limit: int = 100):
    """Get all dishes."""
    db_dishes = db.query(Dish).offset(skip).limit(limit).all()
    return db_dishes

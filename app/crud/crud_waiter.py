"""CRUD functions for DB operations with waiter."""

from sqlalchemy.orm import Session

from app.crud import utils
from app.db.models import Waiter
from app.schemas import WaiterIn


def get_waiter(db: Session, waiter_id: int):
    """Get a waiter by id."""
    db_waiter = db.query(Waiter).filter(Waiter.id == waiter_id).first()
    return db_waiter


def get_all_waiters(db: Session, skip: int = 0, limit: int = 100):
    """Get all waiters."""
    db_waiters = db.query(Waiter).offset(skip).limit(limit).all()
    return db_waiters


def create_waiter(db: Session, waiter: WaiterIn):
    """Create a new waiter."""
    waiter.password = utils.get_password_hash(waiter.password)
    new_waiter = Waiter(**waiter.dict())
    db.add(new_waiter)
    db.commit()
    return new_waiter

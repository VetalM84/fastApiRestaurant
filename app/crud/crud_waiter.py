"""CRUD functions for DB operations with waiter."""

from sqlalchemy.orm import Session

from app.db.models import Waiter


def get_waiter(db: Session, waiter_id: int):
    """Get a waiter by id."""
    db_waiter = db.query(Waiter).filter(Waiter.id == waiter_id).first()
    return db_waiter


def get_all_waiters(db: Session, skip: int = 0, limit: int = 100):
    """Get all waiters."""
    db_waiters = db.query(Waiter).offset(skip).limit(limit).all()
    return db_waiters


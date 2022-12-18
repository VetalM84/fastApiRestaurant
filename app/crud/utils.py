"""Miscellaneous methods for CRUD."""

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from app.db.models import Waiter

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def tip(amount, bill) -> float:
    """Calculate tips."""
    if bill.tip_included:
        return round(amount * bill.tip_percent / 100, 2)
    return 0.00


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify whether a plain password much hashed."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get password hash."""
    return pwd_context.hash(password)


def get_user_by_username(db, username: str) -> Waiter:
    """Get user object based on given username."""
    user = db.query(Waiter).filter(Waiter.username == username).first()
    return user


def authenticate_user(
    username: str, password: str, db: Session
) -> Optional[Waiter | bool]:
    """Check password and return Waiter object."""
    waiter = get_user_by_username(db, username)
    if not waiter or not verify_password(password, waiter.password):
        return False
    return waiter


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})

    encoded_jwt = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

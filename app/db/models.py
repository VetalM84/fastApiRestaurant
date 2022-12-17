"""Models for SQLAlchemy."""

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

bills_dishes_association = Table(
    "bills_dishes",
    Base.metadata,
    Column("bill_id", Integer, ForeignKey("bills.id", ondelete="CASCADE")),
    Column("dish_id", Integer, ForeignKey("dishes.id", ondelete="CASCADE")),
)


class Waiter(Base):
    """Waiter model."""

    __tablename__ = "waiters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(1024), nullable=False)
    bills = relationship("Bill")

    def __repr__(self):
        return f"Waiter(id={self.id}, username={self.username})"


class Bill(Base):
    """Bill model."""

    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    waiter_id = Column(Integer, ForeignKey("waiters.id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    tip_percent = Column(Integer)
    tip_included = Column(Boolean, default=False, nullable=False)
    time = Column(DateTime(timezone=True), server_default=func.now())

    dishes = relationship(
        "Dish", secondary=bills_dishes_association, back_populates="ordered", passive_deletes=True
    )

    def __repr__(self):
        return f"Bill(id={self.id}, table_number={self.table_number}, amount={self.amount})"


class Dish(Base):
    """Dish model."""

    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1024), nullable=False)
    image_url = Column(String(500), nullable=False)
    cost = Column(Float)

    ordered = relationship(
        "Bill",
        secondary=bills_dishes_association,
        back_populates="dishes",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Dish(id={self.id}, name={self.name})"

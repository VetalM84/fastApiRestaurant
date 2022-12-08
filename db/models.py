"""Models for SQLAlchemy."""

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship

from db.database import Base

bills_dishes_association = Table(
    "bills_dishes",
    Base.metadata,
    Column("bill_id", Integer, ForeignKey("bills.id")),
    Column("dish_id", Integer, ForeignKey("dishes.id")),
)


class Waiter(Base):
    """Waiter model."""

    __tablename__ = "waiters"

    id = Column(Integer, primary_key=True)
    username = Column("username", String(50))
    password = Column("password", String(6))
    bills = relationship("Bill")

    def __repr__(self):
        return f"Waiter(id={self.id}, username={self.username})"


class Bill(Base):
    """Bill model."""

    __tablename__ = "bills"

    id = Column("id", Integer, primary_key=True)
    waiter_id = Column(Integer, ForeignKey("waiters.id"))
    table_number = Column("table", Integer)
    amount = Column("amount", Float)
    tip_percent = Column("tip", Integer)
    tip_included = Column("tip_included", Boolean, default=False)
    time = Column("time", DateTime(), server_default=text("NOW()"))

    dishes = relationship(
        "Dish", secondary=bills_dishes_association, back_populates="ordered"
    )

    def __repr__(self):
        return f"Bill(id={self.id}, table_number={self.table_number}, amount={self.amount})"


class Dish(Base):
    """Dish model."""

    __tablename__ = "dishes"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(100))
    description = Column("description", String(1024))
    image_url = Column("image_url", String(500))
    cost = Column("cost", Float)

    ordered = relationship(
        "Bill", secondary=bills_dishes_association, back_populates="dishes"
    )

    def __repr__(self):
        return f"Dish(id={self.id}, name={self.name})"

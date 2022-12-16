"""Schemas for request body data validation. Works both for input and output."""

import datetime
from typing import List

from pydantic import BaseModel, Field, HttpUrl


class DishBase(BaseModel):
    """Base serializer for a dish."""

    id: int
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1024, min_length=2)
    image_url: HttpUrl = Field(..., title="Image URL")
    cost: float

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True


class DishOutBill(DishBase):
    """Base serializer for a dish."""

    description: str = Field(exclude=True)
    image_url: HttpUrl = Field(exclude=True)
    count: int | None = None


class DishIn(DishBase):
    """Serializer for creating a dish."""

    id: int | None = None


class BillBase(BaseModel):
    """Base serializer for a bill."""

    id: int
    waiter_id: int
    table_number: int
    amount: float = 0.00
    tip_percent: int = 5
    tip_included: bool = False
    time: datetime.datetime = None
    dishes: list[DishOutBill] = []

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True


class WaiterBillOut(BillBase):
    """Schema for bills without dishes in waiter response."""

    dishes: list[DishOutBill] = Field(exclude=True)


class BillIn(BillBase):
    """Serializer for creating a bill."""

    id: int | None = None
    dishes: list[int] = Field(..., gt=0, min_items=1)


class WaiterBase(BaseModel):
    """Base serializer for a waiter."""

    id: int
    username: str = Field(..., max_length=50)
    password: str
    bills: List[BillBase] = []

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True


class WaiterOut(WaiterBase):
    """Serializer for a waiter with hidden password."""

    password: str = Field(exclude=True)
    bills: list[WaiterBillOut] = []


class WaiterIn(BaseModel):
    """Base serializer for a new waiter."""

    username: str = Field(..., max_length=50)
    password: str

    class Config:
        """Enable ORM mode for all child methods."""

        orm_mode = True

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class UserRole(str, Enum):
    admin = "admin"
    employee = "employee"


class MovementType(str, Enum):
    add = "add"
    remove = "remove"
    borrow = "borrow"
    return_ = "return"


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    role: UserRole


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    category_id: int = Field(foreign_key="category.id")
    location_id: int = Field(foreign_key="location.id")

    quantity: int = 0
    min_quantity: int = 0
    status: str = "available"


class StockMovement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    product_id: int = Field(foreign_key="product.id")
    user_id: int = Field(foreign_key="user.id")

    movement_type: MovementType
    quantity: int
    timestamp: datetime = Field(default_factory=datetime.now)
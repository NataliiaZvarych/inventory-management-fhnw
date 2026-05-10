from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    type: str = Field(default="sale", max_length=50)

    products: List["Product"] = Relationship(back_populates="category")

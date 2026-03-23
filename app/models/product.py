from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Product(SQLModel, table=True):
	__table_args__ = {"extend_existing": True}

	id: Optional[int] = Field(default=None, primary_key=True)
	name: str = Field(index=True)
	quantity: int = Field(default=0)
	min_quantity: int = Field(default=5)
	status: str = Field(default="available")

	category_id: Optional[int] = Field(default=None, foreign_key="category.id")
	location_id: Optional[int] = Field(default=None, foreign_key="location.id")

	category: Optional["Category"] = Relationship(back_populates="products")
	location: Optional["Location"] = Relationship(back_populates="products")
	stock_movements: List["StockMovement"] = Relationship(back_populates="product")

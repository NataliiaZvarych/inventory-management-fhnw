from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class StockMovement(SQLModel, table=True):
	__table_args__ = {"extend_existing": True}

	id: Optional[int] = Field(default=None, primary_key=True)
	product_id: int = Field(foreign_key="product.id")
	user_id: int = Field(foreign_key="user.id")
	type: str = Field(index=True)
	amount: int
	timestamp: datetime = Field(default_factory=datetime.now)

	product: "Product" = Relationship(back_populates="stock_movements")
	user: "User" = Relationship(back_populates="stock_movements")

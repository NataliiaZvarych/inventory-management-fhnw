from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
	__table_args__ = {"extend_existing": True}

	id: Optional[int] = Field(default=None, primary_key=True)
	username: str = Field(unique=True, index=True)
	password_hash: str
	role: str = Field(default="Staff")

	stock_movements: List["StockMovement"] = Relationship(back_populates="user")

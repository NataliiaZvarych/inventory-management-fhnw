from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Location(SQLModel, table=True):
	__table_args__ = {"extend_existing": True}

	id: Optional[int] = Field(default=None, primary_key=True)
	name: str = Field(index=True)

	products: List["Product"] = Relationship(back_populates="location")

"""Location model definition for the inventory domain.

This file contains the SQLModel class that represents physical storage locations.
"""

from __future__ import annotations

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Location(SQLModel, table=True):
	"""Database table for storage locations.

	A location indicates where products are stored
	(for example, "Main Warehouse" or "Shelf A3").
	"""

	# Primary key for the location table.
	# It is optional in Python instances until persisted by the database.
	id: Optional[int] = Field(default=None, primary_key=True)

	# Human-readable location name displayed across the application.
	# Index is enabled to make filtering/searching by location faster.
	name: str = Field(nullable=False, index=True)

	# One-to-many relationship:
	# one location can store many products.
	products: List["Product"] = Relationship(back_populates="location")

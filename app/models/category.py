"""Category model definition for the inventory domain.

This file contains the SQLModel class that represents product categories.
"""

from __future__ import annotations

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
	"""Database table for product categories.

	A category groups products by business meaning (for example, "Hardware"
	or "Office Supplies").
	"""

	# Primary key for the category table.
	# It is optional at object creation time because the database assigns it.
	id: Optional[int] = Field(default=None, primary_key=True)

	# Human-readable category name used in UI and business logic.
	# Index is enabled to speed up lookups by category name.
	name: str = Field(nullable=False, index=True)

	# One-to-many relationship:
	# one category can contain many products.
	products: List["Product"] = Relationship(back_populates="category")

"""Movement model definition for the inventory domain.

This file contains the SQLModel class that records stock movements.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
	# Imported only for static type checking to avoid circular runtime imports.
	from app.models.product import Product
	from app.models.user import User


class Movement(SQLModel, table=True):
	"""Database table for inventory stock movements.

	A movement captures each inventory change event (for example, stock in,
	stock out, or adjustment) together with product, user, and time.
	"""

	# Primary key for the movement table.
	# Assigned by the database when the movement record is created.
	id: Optional[int] = Field(default=None, primary_key=True)

	# Foreign key to product.id.
	# Every movement must reference exactly one product.
	product_id: int = Field(foreign_key="product.id", nullable=False, index=True)

	# Foreign key to user.id.
	# Every movement is associated with the user who performed it.
	user_id: int = Field(foreign_key="user.id", nullable=False, index=True)

	# Movement type (for example, "in", "out", "adjustment").
	# Kept as text to allow clear business naming.
	type: str = Field(nullable=False, index=True)

	# Number of units affected by this movement.
	# Positive integer expected by business logic.
	amount: int = Field(nullable=False)

	# UTC timestamp indicating when the movement was recorded.
	# A default factory is used so the timestamp is set automatically on create.
	timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

	# Many-to-one relationship to Product.
	# A movement belongs to one product.
	product: Optional["Product"] = Relationship(back_populates="movements")

	# Many-to-one relationship to User.
	# A movement belongs to one user.
	user: Optional["User"] = Relationship(back_populates="movements")

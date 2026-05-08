from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class StockMovement(SQLModel, table=True):
    __tablename__ = "stock_movement"

    movement_id: Optional[int] = Field(default=None, primary_key=True)

    product_id: int = Field(foreign_key="product.product_id")
    user_id: int = Field(foreign_key="user.user_id")

    quantity: int = Field(gt=0)
    movement_type: str = Field(max_length=50)
    note: Optional[str] = Field(default=None)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    product: Optional["Product"] = Relationship(back_populates="movements")
    user: Optional["User"] = Relationship(back_populates="movements")
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User


class Movement(SQLModel, table=True):
    __tablename__ = "movements"

    id: Optional[int] = Field(default=None, primary_key=True)

    product_id: int = Field(foreign_key="products.id", nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)

    movement_type: str = Field(nullable=False)
    quantity: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    note: Optional[str] = Field(default=None, nullable=True)

    product: Optional["Product"] = Relationship(back_populates="movements")
    user: Optional["User"] = Relationship(back_populates="movements")
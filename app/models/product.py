from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.location import Location
    from app.models.movement import Movement


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = Field(default=None, nullable=True)

    quantity: int = Field(default=0, nullable=False)
    min_quantity: int = Field(default=0, nullable=False)
    status: str = Field(default="available", nullable=False)

    category_id: int = Field(foreign_key="categories.id", nullable=False)
    location_id: int = Field(foreign_key="locations.id", nullable=False)

    category: Optional["Category"] = Relationship(back_populates="products")
    location: Optional["Location"] = Relationship(back_populates="products")
    movements: list["Movement"] = Relationship(back_populates="product")
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Product(SQLModel, table=True):
    __tablename__ = "product"

    product_id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)

    quantity: int = Field(default=0, ge=0)
    minimum_stock: int = Field(default=0, ge=0)
    status: str = Field(default="active", max_length=50)

    category_id: int = Field(foreign_key="category.category_id")
    storage_location_id: int = Field(foreign_key="storage_location.storage_location_id")

    category: Optional["Category"] = Relationship(back_populates="products")
    storage_location: Optional["StorageLocation"] = Relationship(back_populates="products")
    movements: List["StockMovement"] = Relationship(back_populates="product")
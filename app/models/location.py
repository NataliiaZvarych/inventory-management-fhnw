from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.product import Product


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, index=True)
    description: Optional[str] = Field(default=None, nullable=True)

    products: list["Product"] = Relationship(back_populates="location")
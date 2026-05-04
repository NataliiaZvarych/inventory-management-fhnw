from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class StorageLocation(SQLModel, table=True):
    __tablename__ = "storage_location"

    storage_location_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    shelf_number: Optional[str] = Field(default=None, max_length=50)

    products: List["Product"] = Relationship(back_populates="storage_location")
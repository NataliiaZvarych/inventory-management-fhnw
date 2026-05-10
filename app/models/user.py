from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(nullable=False, index=True, unique=True)
    email: str = Field(nullable=False, index=True, unique=True)

    password_hash: str = Field(nullable=False)

    role: str = Field(default="user")

    # 🔥 FIX: StockMovement relation (SENİN HATAN BURADAN GELİYOR)
    movements: List["StockMovement"] = Relationship(back_populates="user")

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "user"

    user_id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    role: str = Field(default="staff", max_length=50)
    password_hash: Optional[str] = Field(default=None, max_length=255)

    movements: List["StockMovement"] = Relationship(back_populates="user")
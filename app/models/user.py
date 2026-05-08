from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from .stock_movement import StockMovement


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)

    password_hash: str = Field(nullable=False)

    role: str = Field(default="user")

    # 🔥 RELATIONSHIP (kritik fix)
    movements: List["StockMovement"] = Relationship(back_populates="user")

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.movement import Movement


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, unique=True, index=True)
    email: str = Field(nullable=False, unique=True, index=True)
    role: str = Field(default="employee", nullable=False)

    movements: list["Movement"] = Relationship(back_populates="user")
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)

    # hashed password tutulur
    password_hash: str = Field(nullable=False)

    # role örneği (opsiyonel ama projede var gibi görünüyor)
    role: str = Field(default="user")

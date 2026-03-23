from typing import Optional

from sqlmodel import Session, create_engine, select

from models import User


DATABASE_URL = "sqlite:///inventory.db"
engine = create_engine(DATABASE_URL, echo=False)


class UserService:
	@staticmethod
	def create_user(username: str, password_hash: str, role: str = "Staff") -> User:
		user = User(username=username, password_hash=password_hash, role=role)

		with Session(engine) as session:
			session.add(user)
			session.commit()
			session.refresh(user)
			return user

	@staticmethod
	def list_users() -> list[User]:
		with Session(engine) as session:
			return session.exec(select(User)).all()

	@staticmethod
	def get_user_by_username(username: str) -> Optional[User]:
		with Session(engine) as session:
			statement = select(User).where(User.username == username)
			return session.exec(statement).first()

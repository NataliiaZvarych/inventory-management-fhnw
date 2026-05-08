from typing import Optional

from sqlmodel import Session, select

from app.models import User


class UserService:
	"""Service with simple operations for users."""

	def __init__(self, session: Session):
		self.session = session

	def create_user(self, username: str, email: str, role: str = "employee") -> User:
		"""Create and save a new user."""
		self._validate_username(username)
		self._validate_email(email)
		self._validate_unique_user(username=username, email=email)

		user = User(username=username.strip(), email=email.strip(), role=role.strip() or "employee")
		self.session.add(user)
		self.session.commit()
		self.session.refresh(user)
		return user

	def get_all_users(self) -> list[User]:
		"""Return all users ordered by id."""
		statement = select(User).order_by(User.id)
		return list(self.session.exec(statement).all())

	def get_user_by_id(self, user_id: int) -> Optional[User]:
		"""Return one user by id, or None."""
		return self.session.get(User, user_id)

	@staticmethod
	def _validate_username(username: str) -> None:
		if not username or not username.strip():
			raise ValueError("Username cannot be empty")

	@staticmethod
	def _validate_email(email: str) -> None:
		if not email or not email.strip():
			raise ValueError("Email cannot be empty")

	def _validate_unique_user(self, username: str, email: str) -> None:
		existing_username = self.session.exec(
			select(User).where(User.username == username.strip())
		).first()
		if existing_username is not None:
			raise ValueError("Username already exists")

		existing_email = self.session.exec(
			select(User).where(User.email == email.strip())
		).first()
		if existing_email is not None:
			raise ValueError("Email already exists")

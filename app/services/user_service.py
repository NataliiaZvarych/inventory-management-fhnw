from typing import Optional
from sqlmodel import Session
from app.models import User
from app.data_access.dao import UserDAO
import hashlib

class UserService:
	def __init__(self, user_dao: UserDAO):
		self.user_dao = user_dao

	def get_user(self, session: Session, user_id: int) -> User:
		"""
		Get a user by ID.
		"""
		user = self.user_dao.get(session, user_id)
		if not user:
			raise ValueError("User not found")
		return user

	def update_user(self, session: Session, user_id: int, data: dict) -> User:
		"""
		Update user data by ID.
		"""
		user = self.user_dao.update(session, user_id, data)
		if not user:
			raise ValueError("User not found or update failed")
		return user

	def delete_user(self, session: Session, user_id: int) -> bool:
		"""
		Delete a user by ID.
		"""
		result = self.user_dao.delete(session, user_id)
		if not result:
			raise ValueError("User not found")
		return result

	def login(self, session: Session, name: str, password: str) -> Optional[User]:
		"""
		Authenticate user by name and password.
		"""
		# Simple authentication: find user by name and compare password hash
		users = self.user_dao.get_all(session)
		user = next((u for u in users if u.name == name), None)
		if not user:
			raise ValueError("User not found")
		if not user.password_hash:
			raise ValueError("User has no password set")
		password_hash = hashlib.sha256(password.encode()).hexdigest()
		if user.password_hash != password_hash:
			raise ValueError("Incorrect password")
		return user

	def change_role(self, session: Session, user_id: int, new_role: str) -> User:
		"""
		Change the role of a user.
		"""
		allowed_roles = {"admin", "staff", "manager"}
		if new_role not in allowed_roles:
			raise ValueError(f"Role '{new_role}' is not allowed")
		user = self.user_dao.get(session, user_id)
		if not user:
			raise ValueError("User not found")
		user.role = new_role
		session.add(user)
		session.commit()
		session.refresh(user)
		return user

from typing import List
from sqlmodel import Session
from app.models import StorageLocation
from app.data_access.dao import StorageLocationDAO

class LocationServices:
	def __init__(self, location_dao: StorageLocationDAO):
		self.location_dao = location_dao

	def create_location(self, session: Session, location_data: dict) -> StorageLocation:
		"""
		Create a new storage location after validating required fields.
		"""
		if not location_data.get("name"):
			raise ValueError("Location name is required")
		location = StorageLocation(**location_data)
		return self.location_dao.create(session, location)

	def get_location(self, session: Session, location_id: int) -> StorageLocation:
		"""
		Get a storage location by its ID.
		"""
		location = self.location_dao.get(session, location_id)
		if not location:
			raise ValueError("Location not found")
		return location

	def update_location(self, session: Session, location_id: int, data: dict) -> StorageLocation:
		"""
		Update a storage location by its ID.
		"""
		location = self.location_dao.update(session, location_id, data)
		if not location:
			raise ValueError("Location not found or update failed")
		return location

	def delete_location(self, session: Session, location_id: int) -> bool:
		"""
		Delete a storage location by its ID.
		"""
		result = self.location_dao.delete(session, location_id)
		if not result:
			raise ValueError("Location not found")
		return result

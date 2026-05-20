from typing import List
from sqlmodel import Session
from app.models import Product
from app.data_access.dao import ProductDAO, CategoryDAO, StorageLocationDAO

class ProductServices:

	def get_by_category_id(self, session: Session, category_id: int) -> List[Product]:
		"""
		Get all products by category ID.
		"""
		return self.product_dao.get_by_category_id(session, category_id)
	
	def __init__(self, product_dao: ProductDAO, category_dao: CategoryDAO, location_dao: StorageLocationDAO):
		self.product_dao = product_dao
		self.category_dao = category_dao
		self.location_dao = location_dao

	def create_product(self, session: Session, product_data: dict) -> Product:
		"""
		Create a new product after validating category and location.
		"""
		category = self.category_dao.get(session, product_data['category_id'])
		if not category:
			raise ValueError("Category not found")
		location = self.location_dao.get(session, product_data['storage_location_id'])
		if not location:
			raise ValueError("Storage location not found")
		product = Product(**product_data)
		return self.product_dao.create(session, product)

	def get_product(self, session: Session, product_id: int) -> Product:
		"""
		Get a single product by its ID.
		"""
		product = self.product_dao.get(session, product_id)
		if not product:
			raise ValueError("Product not found")
		return product

	def get_all_products(self, session: Session) -> List[Product]:
		"""
		Get all products from the database.
		"""
		return self.product_dao.get_all(session)

	def update_product(self, session: Session, product_id: int, data: dict) -> Product:
		"""
		Update a product by its ID.
		"""
		product = self.product_dao.update(session, product_id, data)
		if not product:
			raise ValueError("Product not found")
		return product

	def delete_product(self, session: Session, product_id: int) -> bool:
		"""
		Delete a product by its ID.
		"""
		result = self.product_dao.delete(session, product_id)
		if not result:
			raise ValueError("Product not found")
		return result

	def check_availability(self, session: Session, product_id: int) -> bool:
		"""
		Check if the product is available (quantity > 0 and status is active).
		"""
		product = self.product_dao.get(session, product_id)
		if not product:
			raise ValueError("Product not found")
		return product.quantity > 0 and product.status == "active"

	def get_product_details(self, session: Session, product_id: int) -> dict:
		"""
		Get detailed information about a product, including category and location.
		"""
		product = self.product_dao.get(session, product_id)
		if not product:
			raise ValueError("Product not found")
		category = self.category_dao.get(session, product.category_id)
		location = self.location_dao.get(session, product.storage_location_id)
		return {
			"product_id": product.product_id,
			"name": product.name,
			"description": product.description,
			"quantity": product.quantity,
			"minimum_stock": product.minimum_stock,
			"status": product.status,
			"category": category.name if category else None,
			"storage_location": location.name if location else None
		}

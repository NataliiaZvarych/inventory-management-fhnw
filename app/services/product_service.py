from typing import Optional

from sqlmodel import Session, select

from app.models import Category, Location, Product


class ProductService:
	"""Service with simple CRUD operations for products."""

	def __init__(self, session: Session):
		self.session = session

	def create_product(
		self,
		name: str,
		description: Optional[str],
		quantity: int,
		min_quantity: int,
		category_id: int,
		location_id: int,
		status: str = "available",
	) -> Product:
		"""Create a product and save it to the database."""
		self._validate_name(name)
		self._validate_quantities(quantity, min_quantity)
		self._validate_category_exists(category_id)
		self._validate_location_exists(location_id)

		product = Product(
			name=name.strip(),
			description=description,
			quantity=quantity,
			min_quantity=min_quantity,
			status=status,
			category_id=category_id,
			location_id=location_id,
		)

		self.session.add(product)
		self.session.commit()
		self.session.refresh(product)
		return product

	def get_all_products(self) -> list[Product]:
		"""Return all products ordered by id."""
		statement = select(Product).order_by(Product.id)
		return list(self.session.exec(statement).all())

	def get_product_by_id(self, product_id: int) -> Optional[Product]:
		"""Return one product by id, or None if not found."""
		return self.session.get(Product, product_id)

	def update_product(
		self,
		product_id: int,
		name: Optional[str] = None,
		description: Optional[str] = None,
		quantity: Optional[int] = None,
		min_quantity: Optional[int] = None,
		status: Optional[str] = None,
		category_id: Optional[int] = None,
		location_id: Optional[int] = None,
	) -> Product:
		"""Update selected fields of an existing product."""
		product = self.session.get(Product, product_id)
		if product is None:
			raise ValueError(f"Product with id {product_id} not found")

		if name is not None:
			self._validate_name(name)
			product.name = name.strip()

		if description is not None:
			product.description = description

		next_quantity = product.quantity if quantity is None else quantity
		next_min_quantity = product.min_quantity if min_quantity is None else min_quantity

		if quantity is not None or min_quantity is not None:
			self._validate_quantities(next_quantity, next_min_quantity)
			product.quantity = next_quantity
			product.min_quantity = next_min_quantity

		if category_id is not None:
			self._validate_category_exists(category_id)
			product.category_id = category_id

		if location_id is not None:
			self._validate_location_exists(location_id)
			product.location_id = location_id

		if status is not None:
			product.status = status

		self.session.add(product)
		self.session.commit()
		self.session.refresh(product)
		return product

	def delete_product(self, product_id: int) -> None:
		"""Delete a product by id."""
		product = self.session.get(Product, product_id)
		if product is None:
			raise ValueError(f"Product with id {product_id} not found")

		self.session.delete(product)
		self.session.commit()

	@staticmethod
	def _validate_name(name: str) -> None:
		if not name or not name.strip():
			raise ValueError("Product name cannot be empty")

	@staticmethod
	def _validate_quantities(quantity: int, min_quantity: int) -> None:
		if quantity < 0:
			raise ValueError("Quantity cannot be negative")
		if min_quantity < 0:
			raise ValueError("Min quantity cannot be negative")

	def _validate_category_exists(self, category_id: int) -> None:
		category = self.session.get(Category, category_id)
		if category is None:
			raise ValueError(f"Category with id {category_id} not found")

	def _validate_location_exists(self, location_id: int) -> None:
		location = self.session.get(Location, location_id)
		if location is None:
			raise ValueError(f"Location with id {location_id} not found")

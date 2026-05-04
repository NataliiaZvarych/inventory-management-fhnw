from typing import Optional

from sqlmodel import Session, select

from app.models import Movement, Product, User


class InventoryService:
	"""Service for stock operations and movement history."""

	def __init__(self, session: Session):
		self.session = session

	def stock_in(self, product_id: int, user_id: int, quantity: int, note: Optional[str] = None) -> Movement:
		"""Increase product quantity and create an 'in' movement."""
		product = self._get_product_or_error(product_id)
		self._validate_user_exists(user_id)
		self._validate_positive_quantity(quantity)

		product.quantity += quantity
		self._sync_product_status(product)

		movement = Movement(
			product_id=product.id,
			user_id=user_id,
			movement_type="in",
			quantity=quantity,
			note=note,
		)

		self.session.add(product)
		self.session.add(movement)
		self.session.commit()
		self.session.refresh(movement)
		return movement

	def stock_out(self, product_id: int, user_id: int, quantity: int, note: Optional[str] = None) -> Movement:
		"""Decrease product quantity and create an 'out' movement."""
		product = self._get_product_or_error(product_id)
		self._validate_user_exists(user_id)
		self._validate_positive_quantity(quantity)

		if quantity > product.quantity:
			raise ValueError("Not enough stock for stock_out operation")

		product.quantity -= quantity
		self._sync_product_status(product)

		movement = Movement(
			product_id=product.id,
			user_id=user_id,
			movement_type="out",
			quantity=quantity,
			note=note,
		)

		self.session.add(product)
		self.session.add(movement)
		self.session.commit()
		self.session.refresh(movement)
		return movement

	def get_movements(self, product_id: Optional[int] = None) -> list[Movement]:
		"""Return movement history, optionally filtered by product."""
		statement = select(Movement).order_by(Movement.created_at.desc())
		if product_id is not None:
			statement = statement.where(Movement.product_id == product_id)
		return list(self.session.exec(statement).all())

	def get_low_stock_products(self) -> list[Product]:
		"""Return products where quantity is at or below minimum quantity."""
		statement = select(Product).where(Product.quantity <= Product.min_quantity).order_by(Product.id)
		return list(self.session.exec(statement).all())

	@staticmethod
	def _validate_positive_quantity(quantity: int) -> None:
		if quantity <= 0:
			raise ValueError("Quantity must be greater than zero")

	def _get_product_or_error(self, product_id: int) -> Product:
		product = self.session.get(Product, product_id)
		if product is None:
			raise ValueError(f"Product with id {product_id} not found")
		return product

	def _validate_user_exists(self, user_id: int) -> None:
		user = self.session.get(User, user_id)
		if user is None:
			raise ValueError(f"User with id {user_id} not found")

	@staticmethod
	def _sync_product_status(product: Product) -> None:
		if product.quantity <= product.min_quantity:
			product.status = "low_stock"
		else:
			product.status = "available"

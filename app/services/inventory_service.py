from typing import Optional

from sqlmodel import Session, create_engine

from models import Product, StockMovement


DATABASE_URL = "sqlite:///inventory.db"
engine = create_engine(DATABASE_URL, echo=False)


class InventoryService:
	@staticmethod
	def receive_stock(product_id: int, user_id: int, amount: int) -> Optional[Product]:
		if amount <= 0:
			return None

		with Session(engine) as session:
			product = session.get(Product, product_id)
			if not product:
				return None

			product.quantity += amount
			movement = StockMovement(
				product_id=product_id,
				user_id=user_id,
				type="in",
				amount=amount,
			)

			session.add(product)
			session.add(movement)
			session.commit()
			session.refresh(product)
			return product

	@staticmethod
	def issue_stock(product_id: int, user_id: int, amount: int) -> Optional[Product]:
		if amount <= 0:
			return None

		with Session(engine) as session:
			product = session.get(Product, product_id)
			if not product:
				return None

			if product.quantity < amount:
				return None

			product.quantity -= amount
			movement = StockMovement(
				product_id=product_id,
				user_id=user_id,
				type="out",
				amount=amount,
			)

			session.add(product)
			session.add(movement)
			session.commit()
			session.refresh(product)
			return product

from typing import Optional

from sqlmodel import Session, create_engine, select

from models import Product


DATABASE_URL = "sqlite:///inventory.db"
engine = create_engine(DATABASE_URL, echo=False)


class ProductService:
	@staticmethod
	def create_product(
		name: str,
		quantity: int = 0,
		min_quantity: int = 5,
		status: str = "available",
		category_id: Optional[int] = None,
		location_id: Optional[int] = None,
	) -> Product:
		product = Product(
			name=name,
			quantity=quantity,
			min_quantity=min_quantity,
			status=status,
			category_id=category_id,
			location_id=location_id,
		)

		with Session(engine) as session:
			session.add(product)
			session.commit()
			session.refresh(product)
			return product

	@staticmethod
	def list_products() -> list[Product]:
		with Session(engine) as session:
			return session.exec(select(Product)).all()

	@staticmethod
	def get_product_by_id(product_id: int) -> Optional[Product]:
		with Session(engine) as session:
			return session.get(Product, product_id)

	@staticmethod
	def update_product_quantity(product_id: int, new_quantity: int) -> Optional[Product]:
		with Session(engine) as session:
			product = session.get(Product, product_id)
			if not product:
				return None

			product.quantity = new_quantity
			session.add(product)
			session.commit()
			session.refresh(product)
			return product

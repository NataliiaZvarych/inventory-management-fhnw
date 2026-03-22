from sqlmodel import select

from inventory_app.infra.db import get_session
from inventory_app.domain.models import Product


def get_all_products():
    with get_session() as session:
        products = session.execute(select(Product)).scalars().all()
        return products
    
def create_product(name, category_id, location_id, quantity, min_quantity):
    with get_session() as session:

        status = "available"
        if quantity <= min_quantity:
            status = "low_stock"

        product = Product(
            name=name,
            category_id=category_id,
            location_id=location_id,
            quantity=quantity,
            min_quantity=min_quantity,
            status=status,
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        return product
    
from inventory_app.domain.models import StockMovement, MovementType


def increase_stock(product_id, user_id, amount):
    with get_session() as session:

        product = session.get(Product, product_id)

        if not product:
            print("Produkt nicht gefunden")
            return None

        # Stock erhöhen
        product.quantity += amount

        # Status neu berechnen
        if product.quantity <= product.min_quantity:
            product.status = "low_stock"
        else:
            product.status = "available"

        # Bewegung speichern
        movement = StockMovement(
            product_id=product_id,
            user_id=user_id,
            movement_type=MovementType.add,
            quantity=amount,
        )

        session.add(product)
        session.add(movement)

        session.commit()

        return product
    
from inventory_app.domain.models import StockMovement


def get_all_movements():
    with get_session() as session:
        movements = session.execute(select(StockMovement)).scalars().all()
        return movements
    
def decrease_stock(product_id, user_id, amount):
    with get_session() as session:

        product = session.get(Product, product_id)

        if not product:
            print("Produkt nicht gefunden")
            return None

        if product.quantity < amount:
            print("Nicht genug Bestand")
            return None

        # Stock reduzieren
        product.quantity -= amount

        # Status aktualisieren
        if product.quantity <= product.min_quantity:
            product.status = "low_stock"
        else:
            product.status = "available"

        # Bewegung speichern
        movement = StockMovement(
            product_id=product_id,
            user_id=user_id,
            movement_type=MovementType.remove,
            quantity=amount,
        )

        session.add(product)
        session.add(movement)

        session.commit()

        return product
    
def borrow_product(product_id, user_id, amount):
    with get_session() as session:

        product = session.get(Product, product_id)

        if not product:
            print("Produkt nicht gefunden")
            return None

        if product.quantity < amount:
            print("Nicht genug Bestand zum Ausleihen")
            return None

        product.quantity -= amount

        if product.quantity <= product.min_quantity:
            product.status = "low_stock"
        else:
            product.status = "available"

        movement = StockMovement(
            product_id=product_id,
            user_id=user_id,
            movement_type=MovementType.borrow,
            quantity=amount,
        )

        session.add(product)
        session.add(movement)

        session.commit()

        return product
    
def return_product(product_id, user_id, amount):
    with get_session() as session:

        product = session.get(Product, product_id)

        if not product:
            print("Produkt nicht gefunden")
            return None

        product.quantity += amount

        if product.quantity <= product.min_quantity:
            product.status = "low_stock"
        else:
            product.status = "available"

        movement = StockMovement(
            product_id=product_id,
            user_id=user_id,
            movement_type=MovementType.return_,
            quantity=amount,
        )

        session.add(product)
        session.add(movement)

        session.commit()

        return product
    
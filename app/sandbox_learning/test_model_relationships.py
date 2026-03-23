import sys
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

# Ensure imports work when running this file directly from the project root.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import Category, Location, Product, StockMovement, User


def run_relationship_test() -> None:
    engine = create_engine("sqlite:///inventory.db", echo=False)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        category = Category(name="Electronics")
        location = Location(name="Main Warehouse")
        user = User(username="demo_staff", password_hash="demo_hash", role="Staff")

        session.add(category)
        session.add(location)
        session.add(user)
        session.commit()

        session.refresh(category)
        session.refresh(location)
        session.refresh(user)

        product = Product(
            name="USB-C Cable",
            quantity=50,
            min_quantity=10,
            status="available",
            category_id=category.id,
            location_id=location.id,
        )
        session.add(product)
        session.commit()
        session.refresh(product)

        movement = StockMovement(
            product_id=product.id,
            user_id=user.id,
            type="in",
            amount=50,
        )
        session.add(movement)
        session.commit()

        db_product = session.exec(
            select(Product).where(Product.id == product.id)
        ).one()
        db_movement = session.exec(
            select(StockMovement).where(StockMovement.product_id == product.id)
        ).first()

        print("Test data created successfully")
        print(f"Product: {db_product.name}, qty={db_product.quantity}")
        print(f"Category ID: {db_product.category_id}, Location ID: {db_product.location_id}")
        if db_movement:
            print(
                f"Movement: type={db_movement.type}, amount={db_movement.amount}, user_id={db_movement.user_id}"
            )


if __name__ == "__main__":
    run_relationship_test()

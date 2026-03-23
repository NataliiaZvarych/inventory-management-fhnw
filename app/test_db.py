from app.db import get_session
from app.models import Category, Location, User, Product, Movement


def seed_test_data():
    with get_session() as session:
        # Create category
        category = Category(name="Electronics", description="Electronic devices")
        session.add(category)

        # Create location
        location = Location(name="Main Warehouse", description="Central storage")
        session.add(location)

        # Create user
        user = User(username="admin", email="admin@example.com", role="admin")
        session.add(user)

        session.commit()

        # Refresh objects to get IDs
        session.refresh(category)
        session.refresh(location)
        session.refresh(user)

        # Create product
        product = Product(
            name="Laptop",
            description="Dell Latitude",
            quantity=10,
            min_quantity=2,
            status="available",
            category_id=category.id,
            location_id=location.id,
        )
        session.add(product)
        session.commit()
        session.refresh(product)

        # Create movement
        movement = Movement(
            product_id=product.id,
            user_id=user.id,
            movement_type="in",
            quantity=10,
            note="Initial stock"
        )
        session.add(movement)
        session.commit()

        print("Test data inserted successfully.")


if __name__ == "__main__":
    seed_test_data()
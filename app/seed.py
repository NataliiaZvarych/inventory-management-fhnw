from sqlmodel import select

from app.db import get_session
from app.models import Category, Location, User, Product, Movement


def seed_database():
    with get_session() as session:
        # Check if seed data already exists
        existing_category = session.exec(
            select(Category).where(Category.name == "Electronics")
        ).first()

        if existing_category:
            print("Seed data already exists. Skipping seeding.")
            return

        # Create categories
        electronics = Category(
            name="Electronics",
            description="Electronic devices"
        )
        office = Category(
            name="Office",
            description="Office supplies"
        )

        session.add(electronics)
        session.add(office)
        session.commit()
        session.refresh(electronics)
        session.refresh(office)

        # Create locations
        main_warehouse = Location(
            name="Main Warehouse",
            description="Central storage area"
        )
        shelf_a1 = Location(
            name="Shelf A1",
            description="Shelf for frequently used items"
        )

        session.add(main_warehouse)
        session.add(shelf_a1)
        session.commit()
        session.refresh(main_warehouse)
        session.refresh(shelf_a1)

        # Create users
        admin = User(
            username="admin",
            email="admin@example.com",
            role="admin"
        )
        employee = User(
            username="employee1",
            email="employee1@example.com",
            role="employee"
        )

        session.add(admin)
        session.add(employee)
        session.commit()
        session.refresh(admin)
        session.refresh(employee)

        # Create products
        laptop = Product(
            name="Laptop",
            description="Dell Latitude laptop",
            quantity=10,
            min_quantity=2,
            status="available",
            category_id=electronics.id,
            location_id=main_warehouse.id,
        )

        mouse = Product(
            name="Mouse",
            description="Wireless office mouse",
            quantity=25,
            min_quantity=5,
            status="available",
            category_id=office.id,
            location_id=shelf_a1.id,
        )

        session.add(laptop)
        session.add(mouse)
        session.commit()
        session.refresh(laptop)
        session.refresh(mouse)

        # Create movements
        movement_1 = Movement(
            product_id=laptop.id,
            user_id=admin.id,
            movement_type="in",
            quantity=10,
            note="Initial stock"
        )

        movement_2 = Movement(
            product_id=mouse.id,
            user_id=employee.id,
            movement_type="in",
            quantity=25,
            note="Initial stock"
        )

        session.add(movement_1)
        session.add(movement_2)
        session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()
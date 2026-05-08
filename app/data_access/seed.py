from app.data_access.db import get_session, create_db_and_tables
from app.models import Category, StorageLocation, User, Product


def seed_database():
    create_db_and_tables()

    with get_session() as session:

        # 📦 Categories
        electronics = Category(name="Electronics", type="sale")
        office = Category(name="Office", type="sale")
        tools = Category(name="Tools", type="loan")

        # 📍 Storage Locations
        shelf_a1 = StorageLocation(name="Shelf A1")
        shelf_a2 = StorageLocation(name="Shelf A2")
        workshop = StorageLocation(name="Workshop")

        # 👤 Users (your team)
        users = [
            User(name="Nataliia", role="admin"),
            User(name="Mahmut", role="staff"),
            User(name="Aydin", role="staff"),
            User(name="Josselyn", role="admin"),
        ]

        session.add_all([electronics, office, tools, shelf_a1, shelf_a2, workshop] + users)
        session.commit()

        # 🔄 Refresh to get IDs
        session.refresh(electronics)
        session.refresh(office)
        session.refresh(tools)
        session.refresh(shelf_a1)
        session.refresh(shelf_a2)
        session.refresh(workshop)

        # 📦 Products
        products = [
            Product(
                name="A4 Paper",
                description="500 sheets",
                quantity=8,
                minimum_stock=10,
                category_id=office.category_id,
                storage_location_id=shelf_a1.storage_location_id,
            ),
            Product(
                name="USB-C Cable",
                description="2m cable",
                quantity=15,
                minimum_stock=5,
                category_id=electronics.category_id,
                storage_location_id=shelf_a2.storage_location_id,
            ),
            Product(
                name="Drill",
                description="18V battery drill",
                quantity=3,
                minimum_stock=2,
                category_id=tools.category_id,
                storage_location_id=workshop.storage_location_id,
            ),
        ]

        session.add_all(products)
        session.commit()

        print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed_database()
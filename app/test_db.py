from sqlmodel import select
from app.db import get_session
from app.models import Product, User, Category, StorageLocation, StockMovement


def test_database_connection():
    with get_session() as session:
        products = session.exec(select(Product)).all()
        users = session.exec(select(User)).all()
        categories = session.exec(select(Category)).all()
        locations = session.exec(select(StorageLocation)).all()
        movements = session.exec(select(StockMovement)).all()

        print("Database connection successful.")
        print(f"Products: {len(products)}")
        print(f"Users: {len(users)}")
        print(f"Categories: {len(categories)}")
        print(f"Locations: {len(locations)}")
        print(f"Movements: {len(movements)}")

        for p in products:
            print(f"- {p.name} (Stock: {p.quantity})")


if __name__ == "__main__":
    test_database_connection()
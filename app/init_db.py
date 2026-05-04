from app.db import create_db_and_tables
from app.models import Category, StorageLocation, User, Product, StockMovement


def main():
    create_db_and_tables()
    print("Database and tables created successfully.")


if __name__ == "__main__":
    main()
from app.db import create_db_and_tables
from app.models import Category, Location, User, Product, Movement

if __name__ == "__main__":
    create_db_and_tables()
    print("Base de datos creada correctamente.")
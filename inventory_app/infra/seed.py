from sqlmodel import Session, select


from inventory_app.domain.models import Category, Location, User, UserRole, Product
from inventory_app.infra.db import engine


def seed_data():
    with Session(engine) as session:
                # Prüfen, ob bereits Daten vorhanden sind
        existing_product = session.exec(select(Product)).first()
        if existing_product:
            print("Daten bereits vorhanden - kein Seed nötig")
            return

        # Kategorien
        category1 = Category(name="Oberteile")
        category2 = Category(name="Hosen")
        category3 = Category(name="Jacken")

        # Lagerorte
        location1 = Location(name="Regal A")
        location2 = Location(name="Regal B")
        location3 = Location(name="Lagerraum 1")

        # Benutzer
        user1 = User(username="admin", role=UserRole.admin)
        user2 = User(username="mia", role=UserRole.employee)

        session.add(category1)
        session.add(category2)
        session.add(category3)

        session.add(location1)
        session.add(location2)
        session.add(location3)

        session.add(user1)
        session.add(user2)

        session.commit()

        # Produkte
        product1 = Product(
            name="T-Shirt Weiß",
            category_id=category1.id,
            location_id=location1.id,
            quantity=20,
            min_quantity=5,
            status="available",
        )

        product2 = Product(
            name="Jeans Blau",
            category_id=category2.id,
            location_id=location2.id,
            quantity=8,
            min_quantity=4,
            status="available",
        )

        product3 = Product(
            name="Jacke Schwarz",
            category_id=category3.id,
            location_id=location3.id,
            quantity=2,
            min_quantity=3,
            status="low_stock",
        )

        session.add(product1)
        session.add(product2)
        session.add(product3)

        session.commit()

        print("Testdaten erfolgreich hinzugefügt!")
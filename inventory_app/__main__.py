from inventory_app.infra.db import create_db_and_tables
from inventory_app.infra.seed import seed_data
from inventory_app.services.use_cases import get_all_products
from inventory_app.services.use_cases import create_product
from inventory_app.services.use_cases import increase_stock
from inventory_app.services.use_cases import get_all_movements
from inventory_app.services.use_cases import decrease_stock
from inventory_app.services.use_cases import borrow_product, return_product


if __name__ == "__main__":
    create_db_and_tables()
    seed_data()

    products = get_all_products()

    print("Produkte in der Datenbank:")
    for p in products:
        print(p.name, p.quantity, p.status)

    # Beispiel: Neues Produkt erstellen

    print("\nNeues Produkt wird erstellt...")

    new_product = create_product(
        name="Pullover Grau",
        category_id=1,
        location_id=1,
        quantity=3,
        min_quantity=5,
    )
    print("Neues Produkt:", new_product.name, new_product.status)

    # Beispiel: Lagerbestand erhöhen
    print("\nBestand wird erhöht...")

    updated_product = increase_stock(
    product_id=1,
    user_id=1,
    amount=5
    )
    print("Neuer Bestand:", updated_product.name, updated_product.quantity)

    # Besipiel: Alle Bewegungen anzeigen
    print("Neuer Bestand:", updated_product.name, updated_product.quantity)
    print("\nLagerbewegungen:")
    movements = get_all_movements()

for m in movements:
    print(
        "ID:", m.id,
        "| Produkt-ID:", m.product_id,
        "| Benutzer-ID:", m.user_id,
        "| Typ:", m.movement_type,
        "| Menge:", m.quantity
    )

    # Besipiel Lagerbestand verringern
    print("\nBestand wird reduziert...")

    reduced_product = decrease_stock(
    product_id=1,
    user_id=1,
    amount=10
    )

if reduced_product:
    print("Neuer Bestand:", reduced_product.name, reduced_product.quantity)

    # Beispiel: Produkt ausleihen
    print("\nProdukt wird ausgeliehen...")

borrowed_product = borrow_product(
    product_id=1,
    user_id=2,
    amount=2
)

if borrowed_product:
    print("Neuer Bestand nach Ausleihe:", borrowed_product.name, borrowed_product.quantity)

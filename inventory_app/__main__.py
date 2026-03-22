from inventory_app.infra.db import create_db_and_tables
from inventory_app.infra.seed import seed_data

from inventory_app.services.use_cases import (
    create_product,
    increase_stock,
    decrease_stock,
    borrow_product,
    return_product
)

if __name__ == "__main__":
    create_db_and_tables()
    seed_data()

    print("\n--- TEST RETURN PRODUCT ---")

    # Crear producto (si ya existe no se duplica)
    product = create_product(
        name="Pullover Grau",
        category_id=1,
        location_id=1,
        quantity=3,
        min_quantity=5,
    )

    print("Start:", product.name, product.quantity, product.status)

    # Reducir stock
    reduced = decrease_stock(
        product_id=product.id,
        user_id=1,
        amount=1
    )

    print("Nach Reduzierung:", reduced.quantity, reduced.status)

    # Devolver producto
    returned = return_product(
        product_id=product.id,
        user_id=1,
        amount=5
    )

    print("Nach Rückgabe:", returned.quantity, returned.status)
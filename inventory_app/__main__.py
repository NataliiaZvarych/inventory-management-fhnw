from inventory_app.infra.db import create_db_and_tables
from inventory_app.infra.seed import seed_data
from inventory_app.services.use_cases import (
    get_all_products,
    borrow_product,
    return_product,
    export_products_to_csv,
)

if __name__ == "__main__":
    create_db_and_tables()
    seed_data()

    print("\n--- PRODUCT LIST ---")
    products = get_all_products()

    for p in products:
        print(f"{p.id} | {p.name} | {p.quantity} | {p.status}")

    print("\n--- BORROW PRODUCT ---")
    borrowed = borrow_product(product_id=1, user_id=2, amount=1)
    if borrowed:
        print(f"After borrow: {borrowed.quantity} ({borrowed.status})")

    print("\n--- RETURN PRODUCT ---")
    returned = return_product(product_id=1, user_id=2, amount=1)
    if returned:
        print(f"After return: {returned.quantity} ({returned.status})")

    print("\n--- EXPORT CSV ---")
    export_products_to_csv()
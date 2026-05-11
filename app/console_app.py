# Run the console application:
# python3 -m app.console_app

from app.services import *
from app.data_access.db import get_session, engine 
from app.data_access.dao import *

product_services = ProductServices(
    ProductDAO(engine),
    CategoryDAO(engine),
    StorageLocationDAO(engine)
)
category_services = CategoryServices(CategoryDAO(engine), ProductDAO(engine))
location_services = LocationServices(StorageLocationDAO(engine))
movement_services = MovementService(
    ProductDAO(engine),
    UserDAO(engine),
    StockMovementDAO(engine),
    StorageLocationDAO(engine)
)

def select_product_by_category(
    session,
    category_services,
    product_services
):
    categories = category_services.get_all_categories(session)

    print("\nAvailable categories:")

    for category in categories:
        print(f"{category.category_id}: {category.name}")

    category_id = int(input("\nChoose category ID: "))

    products = product_services.get_by_category_id(
        session,
        category_id
    )

    if not products:
        print("No products found in this category.")
        return None

    print("\nAvailable products:")

    for product in products:
        print(
            f"{product.product_id}: "
            f"{product.name} | "
            f"Quantity: {product.quantity}"
        )

    product_id = int(input("\nChoose product ID: "))

    for product in products:
        if product.product_id == product_id:
            return product

    print("Invalid product ID.")
    return None

with get_session() as session:

    while True:
        print("=" * 50)
        print("Welcome to the Inventory Management System!")
        print("=" * 50)
        print("Please select an option:")
        print("-" * 50)
        print("1. Create product")
        print("2. Show all products")
        print("3. Create category")
        print("4. Move product")
        print("5. Show movement history")
        print("6. Check product availability")
        print("7. Delete product")
        print("0. Exit")
        print("-" * 50)

        choice = input("Enter your choice: ")
         
         # Code to create a product
        if choice == "1":
            name = input("Enter product name: ")
            description = input("Enter product description (optional): ")
            quantity = int(input("Enter product quantity: "))
            minimum_stock = int(input("Enter minimum stock level: "))
            status = "active"  # Default status for new products  

            print("\nAvailable categories:")
            categories = category_services.get_all_categories(session)
            for category in categories:
                print(f"- {category.category_id}: {category.name}")
            category_id = int(input("Enter category ID: "))

            print("\nAvailable storage locations:")
            storage_locations = location_services.get_all_storage_locations(session)
            for location in storage_locations:
                print(f"- {location.storage_location_id}: {location.name}")
            storage_location_id = int(input("Enter storage location ID: "))

            product_data = {
                "name": name,
                "description": description,
                "quantity": quantity,
                "minimum_stock": minimum_stock,
                "status": status,
                "category_id": category_id,
                "storage_location_id": storage_location_id,
            }

            product = product_services.create_product(session, product_data)

            print(f"Product created successfully: {product.name}")            

        elif choice == "2":
            # Code to view all products
            products = product_services.get_all_products(session)
            print("\nAll Products:")
            for product in products:
                print(f"- {product.name}: {product.quantity} units available")

        elif choice == "3":
            # Code to create a category
            print("\nCategories in the system:")
            categories = category_services.get_all_categories(session)
            for category in categories:
                print(f"{category.name}")

            name = input("Enter new category name: ")
            description = input("Enter category description (optional): ")

            category_data = {
                "name": name,
                "description": description
            }

            category = category_services.create_category(session, category_data)

            print(f"Category created successfully: {category.name}")

        elif choice == "4":
            # Move product to another location
            product = select_product_by_category(
                session,
                category_services,
                product_services
            )
            if not product:
                continue
            print("\nAvailable storage locations:")
            storage_locations = location_services.get_all_storage_locations(session)
            for location in storage_locations:
                print(f"- {location.storage_location_id}: {location.name}")
            from_location_id = product.storage_location_id
            to_location_id = int(input("Enter target storage location ID: "))
            quantity = int(input("Enter quantity to move: "))
            try:
                movement = movement_services.move_product(
                    session=session,
                    product_id=product.product_id,
                    user_id=1,
                    from_location_id=from_location_id,
                    to_location_id=to_location_id,
                    quantity=quantity
                )
                print(
                    f"Product moved successfully: "
                    f"{movement.quantity} units of '{product.name}' "
                    f"moved to location ID {to_location_id}"
                )
            except ValueError as e:
                print(f"Error moving product: {e}")

        elif choice == "5":
            # Code to check product availability
            product = select_product_by_category(
                session,
                category_services,
                product_services
            )
            if not product:
                continue
            try:
                movements = movement_services.get_product_history(session, product.product_id)
                print(f"\nMovement history for '{product.name}':")
                for movement in movements:
                    print(
                        f"- {movement.timestamp}: "
                        f"Moved {movement.quantity} units "
                        f"Type: {movement.movement_type} "
                        f"Note: {movement.note or ''}"
                    )
            except ValueError as e:
                print(f"Error fetching movement history: {e}")

        elif choice == "6":
            # Check product availability
            product = select_product_by_category(
                session,
                category_services,
                product_services
            )
            if not product:
                continue
            try:
                available = product_services.check_availability(session, product.product_id)
                if available:
                    print(f"Product '{product.name}' is available.")
                else:
                    print(f"Product '{product.name}' is NOT available.")
            except ValueError as e:
                print(f"Error checking availability: {e}")

        elif choice == "7":
            # Delete product
            product = select_product_by_category(
                session,
                category_services,
                product_services
            )
            if not product:
                continue
            confirm = input(f"Are you sure you want to delete product '{product.name}'? (y/n): ").lower()
            if confirm == "y":
                try:
                    product_services.delete_product(session, product.product_id)
                    print(f"Product '{product.name}' deleted successfully.")
                except ValueError as e:
                    print(f"Error deleting product: {e}")
            else:
                print("Deletion cancelled.")

        elif choice == "0":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


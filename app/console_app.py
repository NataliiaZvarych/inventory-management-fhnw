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


    print("=" * 50)
    print("Login")
    print("=" * 50)

    user_id = int(input("Enter your user ID: "))
    role = input("Enter your role (admin/staff): ").lower()

    while True:
        print("=" * 50)
        print("Welcome to the Inventory Management System!")
        print("=" * 50)
        print("Please select an option:")
        print("-" * 50)
        print("1.Product menu")
        print("2.Category menu")
        print("3.Location menu")
        print("4.Movement menu")
        print("0. Exit")
        print("-" * 50)

        choice = input("Enter your choice: ")

        # if role == "admin":
        #     print("3. Create category")

        # print("4. Move product")
        # print("5. Show movement history")
       
         
         
        if choice == "1":
            product_menu(session,role)

        elif choice == "2":
            category_menu(session, role)

        elif choice == "3":
            location_menu(session, role)

        elif choice == "4":
            movement_menu(session, role, user_id)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")  

def product_menu(session, role):
    while True:
                print("\nProduct Menu")
                print("-" * 50)                                      
        
                print("1. Create product")
                print("2. Show all products")
                
                if role == "admin":
                    print("3. Update product")
                    print("4. Delete product")
                print("5. Check product availability")
                print("0. Back to main menu")

                choice = input("Enter your choice: ")

                
                if choice == "1":
                    # Code to create a product
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
                #update product

                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    product = select_product_by_category(
                        session,
                        category_services,
                        product_services
                    )

                    if not product:
                        continue

                    print(f"\nUpdating product: {product.name}")
                    print("Press Enter to keep the current value.")

                    new_name = input(f"Name ({product.name}): ") or product.name

                    new_description = input(
                        f"Description ({product.description or ''}): "
                    ) or product.description

                    new_quantity = input(f"Quantity ({product.quantity}): ")
                    new_minimum_stock = input(f"Minimum stock ({product.minimum_stock}): ")
                    new_status = input(f"Status ({product.status}): ") or product.status

                    print("\nAvailable categories:")
                    categories = category_services.get_all_categories(session)
                    for category in categories:
                        print(f"- {category.category_id}: {category.name}")

                    new_category_id = input(f"Category ID ({product.category_id}): ")

                    print("\nAvailable storage locations:")
                    locations = location_services.get_all_storage_locations(session)
                    for location in locations:
                        print(f"- {location.storage_location_id}: {location.name}")

                    new_storage_location_id = input(
                        f"Storage location ID ({product.storage_location_id}): "
                    )

                    update_data = {
                        "name": new_name,
                        "description": new_description,
                        "quantity": int(new_quantity) if new_quantity else product.quantity,
                        "minimum_stock": (
                            int(new_minimum_stock)
                            if new_minimum_stock
                            else product.minimum_stock
                        ),
                        "status": new_status,
                        "category_id": (
                            int(new_category_id)
                            if new_category_id
                            else product.category_id
                        ),
                        "storage_location_id": (
                            int(new_storage_location_id)
                            if new_storage_location_id
                            else product.storage_location_id
                        ),
                    }

                    try:
                        updated_product = product_services.update_product(
                            session,
                            product.product_id,
                            update_data
                        )

                        print(f"Product '{updated_product.name}' updated successfully.")

                    except ValueError as e:
                        print(f"Error updating product: {e}")
                elif choice == "4":
                    # Code to delete a product

                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    product = select_product_by_category(
                        session,
                        category_services,
                        product_services
                    )

                    if not product:
                        continue

                    print(f"\nSelected product: {product.name}")
                    print(f"Quantity: {product.quantity}")
                    print(f"Status: {product.status}")

                    confirm = input(
                        f"Are you sure you want to delete '{product.name}'? (y/n): "
                    ).lower()

                    if confirm != "y":
                        print("Deletion cancelled.")
                        continue

                    try:
                        product_services.delete_product(
                            session,
                            product.product_id
                        )

                        print(f"Product '{product.name}' deleted successfully.")

                    except ValueError as e:
                        print(f"Error deleting product: {e}")
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
                        available = product_services.check_availability(
                            session,
                            product.product_id
                        )

                        if available:
                            print(f"Product '{product.name}' is available.")
                        else:
                            print(f"Product '{product.name}' is NOT available.")

                    except ValueError as e:
                        print(f"Error checking availability: {e}")
                elif choice == "0":
                    break
                else:
                    print("Invalid choice. Please try again.")
def category_menu(session, role):
    while True:
                print("\nCategory Menu")
                print("-" * 50)
                print("1. Show all categories")
                if role == "admin":
                    print("2. Create category")
                    print("3. Update category")
                    print("4. Delete category")
                
                print("0. Back to main menu")

                choice = input("Enter your choice: ")

                if choice == "1":
                    # Code to show all categories
                    categories = category_services.get_all_categories(session)
                    print("\nAll Categories:")
                    for category in categories:
                        print(f"- {category.name}")
                elif choice == "2":

                    # Code to create a category
                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    print("\nCreate New Category")

                    name = input("Enter category name: ")

                    print("\nCategory types:")
                    print("1. sale")
                    print("2. loan")

                    type_choice = input("Choose category type: ")

                    if type_choice == "1":
                        category_type = "sale"
                    elif type_choice == "2":
                        category_type = "loan"
                    else:
                        print("Invalid category type.")
                        continue

                    category_data = {
                        "name": name,
                        "type": category_type
                    }

                    try:

                        category = category_services.create_category(
                            session,
                            category_data
                        )

                        print(
                            f"Category '{category.name}' "
                            f"created successfully."
                        )

                    except ValueError as e:
                        print(f"Error creating category: {e}")
                elif choice == "3":
                # Update category
                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    categories = category_services.get_all_categories(session)

                    if not categories:
                        print("No categories found.")
                        continue

                    print("\nAvailable categories:")

                    for category in categories:
                        print(
                            f"{category.category_id}: "
                            f"{category.name} | "
                            f"Type: {category.type}"
                        )

                    category_id = int(input("\nEnter category ID to update: "))

                    selected_category = None

                    for category in categories:
                        if category.category_id == category_id:
                            selected_category = category
                            break

                    if not selected_category:
                        print("Invalid category ID.")
                        continue

                    print("\nPress Enter to keep current value.")

                    new_name = input(
                        f"Name ({selected_category.name}): "
                    ) or selected_category.name

                    print("\nCategory types:")
                    print("1. sale")
                    print("2. loan")

                    type_choice = input(
                        f"Type ({selected_category.type}): "
                    )

                    if type_choice == "":
                        new_type = selected_category.type
                    elif type_choice == "1":
                        new_type = "sale"
                    elif type_choice == "2":
                        new_type = "loan"
                    else:
                        print("Invalid category type.")
                        continue

                    update_data = {
                        "name": new_name,
                        "type": new_type
                    }

                    try:

                        updated_category = category_services.update_category(
                            session,
                            category_id,
                            update_data
                        )

                        print(
                            f"Category '{updated_category.name}' "
                            f"updated successfully."
                        )

                    except ValueError as e:
                        print(f"Error updating category: {e}")               
                elif choice == "4":
                #delete category

                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    categories = category_services.get_all_categories(session)

                    if not categories:
                        print("No categories found.")
                        continue

                    print("\nAvailable categories:")

                    for category in categories:
                        print(
                            f"{category.category_id}: "
                            f"{category.name} | "
                            f"Type: {category.type}"
                        )

                    category_id = int(input("\nEnter category ID to delete: "))

                    selected_category = None

                    for category in categories:
                        if category.category_id == category_id:
                            selected_category = category
                            break

                    if not selected_category:
                        print("Invalid category ID.")
                        continue

                    confirm = input(
                        f"Are you sure you want to delete "
                        f"'{selected_category.name}'? (y/n): "
                    ).lower()

                    if confirm != "y":
                        print("Deletion cancelled.")
                        continue

                    try:

                        category_services.delete_category(
                            session,
                            category_id
                        )

                        print(
                            f"Category '{selected_category.name}' "
                            f"deleted successfully."
                        )

                    except ValueError as e:
                        print(f"Error deleting category: {e}")
                elif choice == "0":
                    break
                else:
                    print("Invalid choice. Please try again.")
def location_menu(session, role):
    while True:
                print("\nStorage Location Menu")
                print("-" * 50)
                print("1. Show all storage locations")
                if role == "admin":
                    print("2. Create storage location")
                    print("3. Update storage location")
                    print("4. Delete storage location")
                print("0. Back to main menu")

                choice = input("Enter your choice: ")

                if choice == "1":
                    # Code to show all storage locations
                    locations = location_services.get_all_storage_locations(session)
                    print("\nAll Storage Locations:")
                    for location in locations:
                        print(
                            f"- {location.storage_location_id}: "
                            f"{location.name} | "
                            f"Shelf: {location.shelf_number or '-'}"
                        )
                elif choice == "2":
                    # Code to create a storage location
                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    print("\nCreate New Storage Location")

                    name = input("Enter storage location name: ")
                    shelf_number = input("Enter shelf number (optional): ")

                    location_data = {
                        "name": name,
                        "shelf_number": shelf_number or None
                    }

                    try:
                        location = location_services.create_location(
                            session,
                            location_data
                        )

                        print(
                            f"Storage location '{location.name}' "
                            f"created successfully."
                        )

                    except ValueError as e:
                        print(f"Error creating storage location: {e}")
                        
                elif choice == "3": 
                # Update storage location

                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    locations = location_services.get_all_storage_locations(session)

                    if not locations:
                        print("No storage locations found.")
                        continue

                    print("\nAvailable storage locations:")

                    for location in locations:
                        print(
                            f"{location.storage_location_id}: "
                            f"{location.name} | "
                            f"Shelf: {location.shelf_number or '-'}"
                        )

                    location_id = int(
                        input("\nEnter storage location ID to update: ")
                    )

                    selected_location = None

                    for location in locations:
                        if location.storage_location_id == location_id:
                            selected_location = location
                            break

                    if not selected_location:
                        print("Invalid storage location ID.")
                        continue

                    print("\nPress Enter to keep current value.")

                    new_name = input(
                        f"Name ({selected_location.name}): "
                    ) or selected_location.name

                    new_shelf_number = input(
                        f"Shelf number ({selected_location.shelf_number or '-'}): "
                    )

                    update_data = {
                        "name": new_name,
                        "shelf_number": (
                            new_shelf_number
                            if new_shelf_number
                            else selected_location.shelf_number
                        )
                    }

                    try:

                        updated_location = location_services.update_location(
                            session,
                            location_id,
                            update_data
                        )

                        print(
                            f"Storage location '{updated_location.name}' "
                            f"updated successfully."
                        )

                    except ValueError as e:
                        print(f"Error updating storage location: {e}")

                elif choice == "4":

                    if role != "admin":
                        print("Access denied. Admin only.")
                        continue

                    locations = location_services.get_all_storage_locations(session)

                    if not locations:
                        print("No storage locations found.")
                        continue

                    print("\nAvailable storage locations:")

                    for location in locations:
                        print(
                            f"{location.storage_location_id}: "
                            f"{location.name} | "
                            f"Shelf: {location.shelf_number or '-'}"
                        )

                    location_id = int(
                        input("\nEnter storage location ID to delete: ")
                    )

                    selected_location = None

                    for location in locations:
                        if location.storage_location_id == location_id:
                            selected_location = location
                            break

                    if not selected_location:
                        print("Invalid storage location ID.")
                        continue

                    confirm = input(
                        f"Are you sure you want to delete "
                        f"'{selected_location.name}'? (y/n): "
                    ).lower()

                    if confirm != "y":
                        print("Deletion cancelled.")
                        continue

                    try:

                        location_services.delete_location(
                            session,
                            location_id
                        )

                        print(
                            f"Storage location '{selected_location.name}' "
                            f"deleted successfully."
                        )

                    except ValueError as e:
                        print(f"Error deleting storage location: {e}")

                elif choice == "0":
                    break
                else:
                    print("Invalid choice. Please try again.")

def movement_menu(session, role, user_id):
    while True:
        print("\nStock Movement Menu")
        print("-" * 50)
        print("1. Move product to another location")
        print("2. Show movement history for a product")
        print("0. Back to main menu")

        choice = input("Enter your choice: ")

        if choice == "1":
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
                    user_id=user_id,
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

        elif choice == "2":
            product = select_product_by_category(
                session,
                category_services,
                product_services
            )

            if not product:
                continue

            try:
                movements = movement_services.get_product_history(
                    session,
                    product.product_id
                )

                if not movements:
                    print(f"No movement history found for '{product.name}'.")
                    continue

                print(f"\nMovement history for '{product.name}':")
                print("-" * 50)

                for movement in movements:
                    print(f"Movement ID: {movement.movement_id}")
                    print(f"Product ID: {movement.product_id}")
                    print(f"User ID: {movement.user_id}")
                    print(f"Quantity: {movement.quantity}")
                    print(f"Type: {movement.movement_type}")
                    print(f"Note: {movement.note or '-'}")
                    print(f"Timestamp: {movement.timestamp}")
                    print("-" * 50)

            except ValueError as e:
                print(f"Error fetching movement history: {e}")

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")

    with get_session() as session:
            print("=" * 50)
            print("Login")
            print("=" * 50)

            user_id = int(input("Enter your user ID: "))
            role = input("Enter your role (admin/staff): ").lower()
            

            while True:
                                        print("=" * 50)
                                        print("Welcome to the Inventory Management System!")
                                        print("=" * 50)
                                        print("Please select an option:")
                                        print("-" * 50)
                                        print("1.Product menu")
                                        print("2.Category menu")
                                        print("3.Location menu")
                                        print("4.Movement menu")
                                        print("0. Exit")
                                        print("-" * 50)

                                        choice = input("Enter your choice: ")

                                        if choice == "1":
                                            product_menu(session,role)

                                        elif choice == "2":
                                            category_menu(session, role)

                                        elif choice == "3":
                                            location_menu(session, role)

                                        elif choice == "4":
                                            movement_menu(session, role, user_id)

                                        elif choice == "0":
                                            print("Goodbye!")
                                            break

                                        else:
                                            print("Invalid choice.")  

if __name__ == "__main__":
    with get_session() as session:
        print("=" * 50)
        print("Login")
        print("=" * 50)

        user_id = int(input("Enter your user ID: "))

        user = UserDAO(engine).get(session, user_id)

        if not user:
            print("User not found.")
            exit()

        print(f"Welcome, {user.name}!")

        role = user.role.lower()

        while True:
            print("=" * 50)
            print("Welcome to the Inventory Management System!")
            print("=" * 50)
            print("Please select an option:")
            print("-" * 50)
            print("1. Product menu")
            print("2. Category menu")
            print("3. Location menu")
            print("4. Movement menu")
            print("0. Exit")
            print("-" * 50)

            choice = input("Enter your choice: ")

            if choice == "1":
                product_menu(session, role)
            elif choice == "2":
                category_menu(session, role)
            elif choice == "3":
                location_menu(session, role)
            elif choice == "4":
                movement_menu(session, role, user_id)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")







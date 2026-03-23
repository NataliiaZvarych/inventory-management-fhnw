"""
Sandbox Application: Understanding Backend, Frontend, and Database Integration

This script demonstrates how these three layers work together:
- DATABASE: SQLModel manages data persistence in SQLite
- BACKEND: Python functions handle business logic
- FRONTEND: NiceGUI provides the user interface

Run with: python sandbox_app.py
"""

# ============================================================================
# IMPORTS
# ============================================================================
from typing import List
from nicegui import ui
from sqlmodel import SQLModel, Field, create_engine, Session, select
import os


# ============================================================================
# DATABASE LAYER: Define the data model
# ============================================================================

class Product(SQLModel, table=True):
    """
    DATABASE: Product table definition using SQLModel
    This class represents the structure of data stored in the database.
    
    Fields:
    - id: Unique identifier (auto-generated primary key)
    - name: Product name
    - quantity: Available quantity in stock
    """
    __table_args__ = {"extend_existing": True}
    
    id: int | None = Field(default=None, primary_key=True)
    name: str
    quantity: int


# ============================================================================
# DATABASE SETUP: Create and configure SQLite database
# ============================================================================

# DATABASE: Define the database file location
DATABASE_FILE = "sandbox.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# DATABASE: Create SQLite engine
engine = create_engine(DATABASE_URL, echo=False)

# DATABASE: Create tables if they don't exist
SQLModel.metadata.create_all(engine)


# ============================================================================
# BACKEND LAYER: Business logic functions
# ============================================================================

def add_product(name: str, quantity: int) -> Product | None:
    """
    BACKEND: Add a new product to the database
    
    Args:
        name: Product name
        quantity: Product quantity
        
    Returns:
        Product object if successful, None otherwise
        
    Raises:
        ValueError: If name is empty or quantity is invalid
    """
    # BACKEND: Validation logic
    if not name or name.strip() == "":
        print("❌ Error: Product name cannot be empty")
        return None
    
    if quantity < 0:
        print("❌ Error: Quantity cannot be negative")
        return None
    
    try:
        # BACKEND: Create product instance
        product = Product(name=name.strip(), quantity=quantity)
        
        # DATABASE: Save to database
        with Session(engine) as session:
            session.add(product)
            session.commit()
            session.refresh(product)
            print(f"✅ Product added: {product.name} (qty: {product.quantity})")
            return product
    except Exception as e:
        print(f"❌ Error adding product: {e}")
        return None


def get_all_products() -> List[Product]:
    """
    BACKEND: Retrieve all products from the database
    
    Returns:
        List of Product objects
    """
    try:
        # DATABASE: Query all products
        with Session(engine) as session:
            products = session.exec(select(Product)).all()
            return products
    except Exception as e:
        print(f"❌ Error retrieving products: {e}")
        return []


def delete_product(product_id: int) -> bool:
    """
    BACKEND: Delete a product from the database
    
    Args:
        product_id: ID of the product to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # DATABASE: Query and delete product
        with Session(engine) as session:
            product = session.get(Product, product_id)
            if product:
                session.delete(product)
                session.commit()
                print(f"✅ Product deleted: {product.name}")
                return True
            else:
                print(f"❌ Product with ID {product_id} not found")
                return False
    except Exception as e:
        print(f"❌ Error deleting product: {e}")
        return False


# ============================================================================
# FRONTEND LAYER: NiceGUI User Interface
# ============================================================================

# FRONTEND: Initialize the UI page
page_title = "📦 Sandbox - Product Inventory Manager"
ui.page_title(page_title)

# FRONTEND: Create main container
with ui.column().classes("w-full max-w-2xl mx-auto p-6"):
    # FRONTEND: Header
    ui.label(page_title).classes("text-2xl font-bold text-center mb-6")
    ui.separator()
    
    # FRONTEND: Input section
    with ui.card().classes("w-full"):
        ui.label("Add New Product").classes("text-lg font-semibold mb-4")
        
        # FRONTEND: Product name input field
        product_name_input = ui.input(
            label="Product Name",
            placeholder="Enter product name...",
        ).classes("w-full")
        
        # FRONTEND: Quantity input field (number spinner)
        quantity_input = ui.number(
            label="Quantity",
            value=1,
            min=0,
        ).classes("w-full")
        
        # FRONTEND: Feedback message label
        feedback_label = ui.label("").classes("text-sm mt-2")
        
        def handle_add_product():
            """
            FRONTEND: Handle the "Add" button click event
            
            This function:
            1. Retrieves input values from the UI
            2. Calls BACKEND function to add product
            3. Updates the product list display
            4. Clears input fields and shows feedback
            """
            name = product_name_input.value
            quantity = int(quantity_input.value)
            
            # BACKEND: Call backend logic
            result = add_product(name, quantity)
            
            if result:
                # FRONTEND: Show success feedback
                feedback_label.set_text("✅ Product added successfully!")
                feedback_label.classes("text-green-600", remove="text-red-600")
                
                # FRONTEND: Clear input fields
                product_name_input.value = ""
                quantity_input.value = 1
                
                # FRONTEND: Refresh the product list display
                refresh_product_list()
            else:
                # FRONTEND: Show error feedback
                feedback_label.set_text("❌ Failed to add product. Check inputs.")
                feedback_label.classes("text-red-600", remove="text-green-600")
        
        # FRONTEND: Add button
        ui.button("Add Product", on_click=handle_add_product).classes("w-full mt-4 bg-blue-500")
    
    # FRONTEND: Separator
    ui.separator().classes("my-6")
    
    # FRONTEND: Products display section
    ui.label("Current Inventory").classes("text-lg font-semibold mb-4")
    
    # FRONTEND: Container for product list
    products_container = ui.column().classes("w-full")
    
    def refresh_product_list():
        """
        FRONTEND: Refresh and display the product list
        
        This function:
        1. Clears the existing UI list
        2. Calls BACKEND function to get products
        3. Renders each product as a card with delete option
        """
        products_container.clear()
        
        # BACKEND: Retrieve all products
        products = get_all_products()
        
        if not products:
            # FRONTEND: Show empty state message
            ui.label("No products yet. Add one to get started!").classes("text-gray-500 italic")
        else:
            # FRONTEND: Display each product
            for product in products:
                with ui.card().classes("w-full"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column():
                            ui.label(f"📦 {product.name}").classes("font-semibold")
                            ui.label(f"Quantity: {product.quantity}").classes("text-sm text-gray-600")
                        
                        # FRONTEND: Delete button for each product
                        def make_delete_handler(pid, pname):
                            def delete_handler():
                                # BACKEND: Delete via backend function
                                delete_product(pid)
                                # FRONTEND: Refresh the list after deletion
                                refresh_product_list()
                            return delete_handler
                        
                        ui.button(
                            "Delete",
                            on_click=make_delete_handler(product.id, product.name)
                        ).classes("bg-red-500")
    
    # FRONTEND: Initial load of products
    refresh_product_list()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ in {"__main__", "__mp_main__"}:
    print("=" * 70)
    print("🚀 Starting Sandbox Application")
    print("=" * 70)
    print(f"📁 Database: {DATABASE_FILE}")
    print("🌐 Frontend: Open http://localhost:8080 in your browser")
    print("=" * 70)
    
    # FRONTEND: Launch the NiceGUI application
    ui.run(host="localhost", port=8080)

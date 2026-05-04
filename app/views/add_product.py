# Add product view - placeholder for future UI
from nicegui import ui


def show_add_product():
    ui.label("➕ Add Product")

    name_input = ui.input("Product Name")
    description_input = ui.input("Description")
    quantity_input = ui.input("Quantity")
    min_quantity_input = ui.input("Minimum Quantity")
    category_input = ui.input("Category ID")
    location_input = ui.input("Location ID")

    ui.button("Save Product")
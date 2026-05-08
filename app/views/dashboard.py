from nicegui import ui
from app.views.product_list import show_product_list


def show_dashboard():
    with ui.row():
        ui.label("Welcome to the Inventory Management Dashboard!")
        ui.label("Here you can manage your products, view inventory levels, and generate reports.")

    ui.button("Go to Products", on_click=show_product_list)
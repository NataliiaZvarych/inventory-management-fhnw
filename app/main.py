from nicegui import ui

ui.label('Inventory Management App')

with ui.row():
    ui.button('Dashboard')
    ui.button('Products')
    ui.button('Add Product')

ui.run()
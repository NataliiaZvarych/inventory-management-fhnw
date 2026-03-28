from nicegui import ui

@ui.page('/products')
def products_page():
    ui.label('Products Page').classes('text-h4')
    
    # Sample products data
    products = [
        {'id': 1, 'name': 'Product A', 'price': 29.99, 'stock': 15},
        {'id': 2, 'name': 'Product B', 'price': 49.99, 'stock': 8},
        {'id': 3, 'name': 'Product C', 'price': 19.99, 'stock': 0},
    ]
    
    # Create a table to display products
    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'price', 'label': 'Price', 'field': 'price'},
        {'name': 'stock', 'label': 'Stock', 'field': 'stock'},
    ]
    
    ui.table(columns=columns, rows=products).classes('w-full')
    
    # Add new product button
    with ui.row():
        ui.button('Add Product', on_click=lambda: ui.notify('Add product clicked'))
        ui.button('Refresh', on_click=lambda: ui.notify('Refreshed'))
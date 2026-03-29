from nicegui import ui

def show_dashboard():
    content.clear()
    with content:
        ui.label('Dashboard Page')

def show_products():
    content.clear()
    with content:
        ui.label('Products Page')

def show_add_product():
    content.clear()
    with content:
        ui.label('Add Product Page')

# ÜST SABİT ALAN
ui.label('Inventory Management App')

with ui.row():
    ui.button('Dashboard', on_click=show_dashboard)
    ui.button('Products', on_click=show_products)
    ui.button('Add Product', on_click=show_add_product)

# ALT İÇERİK ALANI
content = ui.column()

# başlangıç
show_dashboard()

ui.run()
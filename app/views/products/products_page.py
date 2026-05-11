from nicegui import ui

from app.views.products.add_product import render_add_product_form
from app.views.products.product_list import render_product_list

@ui.page('/products')
def products_page():
    ui.label('Products').classes('text-h4')

    list_panel = ui.column().classes('w-full')

    def refresh_list() -> None:
        list_panel.clear()
        render_product_list(list_panel)

    with ui.row().classes('w-full q-col-gutter-md'):
        with ui.column().classes('col-12 col-md-7'):
            refresh_list()
        with ui.column().classes('col-12 col-md-5'):
            render_add_product_form(on_created=refresh_list)
from nicegui import ui

from views.add_product import render_add_product
from views.movement import render_movement_controls
from views.product_list import ProductListView


def render_dashboard() -> None:
	ui.page_title("Inventory Management")

	with ui.column().classes("w-full max-w-5xl mx-auto p-6 gap-4"):
		ui.label("Inventory Dashboard").classes("text-2xl font-bold")

		product_list = ProductListView()

		with ui.row().classes("w-full gap-4"):
			with ui.column().classes("w-full"):
				render_add_product(on_product_added=product_list.refresh)
			with ui.column().classes("w-full"):
				render_movement_controls(on_inventory_changed=product_list.refresh)

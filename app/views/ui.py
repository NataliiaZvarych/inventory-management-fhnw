from app.views.add_product import create_product, get_category_options, get_location_options
from app.views.dashboard import get_dashboard_stats, get_low_stock_rows
from app.views.movement import (
	get_movement_rows,
	get_product_options,
	get_user_options,
	register_stock_movement,
)
from app.views.product_list import get_product_rows


def render_ui() -> None:
	"""Create and run NiceGUI frontend."""
	from nicegui import ui

	@ui.refreshable
	def dashboard_panel() -> None:
		stats = get_dashboard_stats()
		low_stock_rows = get_low_stock_rows()

		with ui.row().classes("w-full gap-4"):
			with ui.card().classes("w-full"):
				ui.label("Total products").classes("text-subtitle2")
				ui.label(str(stats["total_products"]))
			with ui.card().classes("w-full"):
				ui.label("Low stock items").classes("text-subtitle2")
				ui.label(str(stats["low_stock"]))
			with ui.card().classes("w-full"):
				ui.label("Total movements").classes("text-subtitle2")
				ui.label(str(stats["total_movements"]))

		ui.separator()
		ui.label("Low stock products").classes("text-h6")
		ui.table(
			columns=[
				{"name": "id", "label": "ID", "field": "id"},
				{"name": "name", "label": "Name", "field": "name"},
				{"name": "quantity", "label": "Qty", "field": "quantity"},
				{"name": "min_quantity", "label": "Min Qty", "field": "min_quantity"},
				{"name": "status", "label": "Status", "field": "status"},
			],
			rows=low_stock_rows,
			row_key="id",
		).classes("w-full")

	@ui.refreshable
	def product_list_panel() -> None:
		ui.table(
			columns=[
				{"name": "id", "label": "ID", "field": "id"},
				{"name": "name", "label": "Name", "field": "name"},
				{"name": "description", "label": "Description", "field": "description"},
				{"name": "quantity", "label": "Qty", "field": "quantity"},
				{"name": "min_quantity", "label": "Min Qty", "field": "min_quantity"},
				{"name": "status", "label": "Status", "field": "status"},
				{"name": "category", "label": "Category", "field": "category"},
				{"name": "location", "label": "Location", "field": "location"},
			],
			rows=get_product_rows(),
			row_key="id",
			pagination=10,
		).classes("w-full")

	def add_product_panel() -> None:
		category_options = {category_id: name for category_id, name in get_category_options()}
		location_options = {location_id: name for location_id, name in get_location_options()}

		if not category_options or not location_options:
			ui.label("Create seed data first to add products.").classes("text-negative")
			return

		with ui.card().classes("w-full max-w-xl"):
			name_input = ui.input("Name").classes("w-full")
			description_input = ui.input("Description").classes("w-full")
			quantity_input = ui.number("Quantity", value=0, min=0).classes("w-full")
			min_quantity_input = ui.number("Min quantity", value=0, min=0).classes("w-full")
			category_select = ui.select(category_options, label="Category").classes("w-full")
			location_select = ui.select(location_options, label="Location").classes("w-full")

			def submit() -> None:
				try:
					create_product(
						name=name_input.value or "",
						description=description_input.value,
						quantity=int(quantity_input.value or 0),
						min_quantity=int(min_quantity_input.value or 0),
						category_id=int(category_select.value),
						location_id=int(location_select.value),
					)
				except Exception as error:
					ui.notify(str(error), type="negative")
					return

				name_input.set_value("")
				description_input.set_value("")
				quantity_input.set_value(0)
				min_quantity_input.set_value(0)
				ui.notify("Product created", type="positive")
				product_list_panel.refresh()
				dashboard_panel.refresh()

			ui.button("Add product", on_click=submit)

	@ui.refreshable
	def movement_panel() -> None:
		product_options = {product_id: label for product_id, label in get_product_options()}
		user_options = {user_id: label for user_id, label in get_user_options()}

		if not product_options or not user_options:
			ui.label("Create seed data first to register movements.").classes("text-negative")
			return

		with ui.card().classes("w-full max-w-xl"):
			movement_type = ui.select({"in": "Stock In", "out": "Stock Out"}, value="in", label="Type").classes("w-full")
			product_select = ui.select(product_options, label="Product").classes("w-full")
			user_select = ui.select(user_options, label="User").classes("w-full")
			quantity_input = ui.number("Quantity", value=1, min=1).classes("w-full")
			note_input = ui.input("Note").classes("w-full")

			def submit_movement() -> None:
				try:
					register_stock_movement(
						movement_type=str(movement_type.value),
						product_id=int(product_select.value),
						user_id=int(user_select.value),
						quantity=int(quantity_input.value or 1),
						note=note_input.value,
					)
				except Exception as error:
					ui.notify(str(error), type="negative")
					return

				quantity_input.set_value(1)
				note_input.set_value("")
				ui.notify("Movement saved", type="positive")
				movement_panel.refresh()
				product_list_panel.refresh()
				dashboard_panel.refresh()

			ui.button("Save movement", on_click=submit_movement)

		ui.separator()
		ui.label("Movement history").classes("text-h6")
		ui.table(
			columns=[
				{"name": "id", "label": "ID", "field": "id"},
				{"name": "product", "label": "Product", "field": "product"},
				{"name": "user", "label": "User", "field": "user"},
				{"name": "type", "label": "Type", "field": "type"},
				{"name": "quantity", "label": "Quantity", "field": "quantity"},
				{"name": "created_at", "label": "Created", "field": "created_at"},
				{"name": "note", "label": "Note", "field": "note"},
			],
			rows=get_movement_rows(),
			row_key="id",
			pagination=10,
		).classes("w-full")

	@ui.page("/")
	def index() -> None:
		ui.label("Inventory Management").classes("text-h4")
		with ui.tabs().classes("w-full") as tabs:
			tab_dashboard = ui.tab("Dashboard")
			tab_products = ui.tab("Product list")
			tab_add = ui.tab("Add product")
			tab_movement = ui.tab("Movement")

		with ui.tab_panels(tabs, value=tab_dashboard).classes("w-full"):
			with ui.tab_panel(tab_dashboard):
				dashboard_panel()
			with ui.tab_panel(tab_products):
				product_list_panel()
			with ui.tab_panel(tab_add):
				add_product_panel()
			with ui.tab_panel(tab_movement):
				movement_panel()

	ui.run(title="Inventory Management", port=8080)

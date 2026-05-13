from nicegui import ui

from app.data_access.dao import ProductDAO, StorageLocationDAO
from app.data_access.db import engine, get_session

from .layout import render_shell


def _build_rows() -> list[dict]:
	location_dao = StorageLocationDAO(engine)
	product_dao = ProductDAO(engine)

	with get_session() as session:
		locations = location_dao.get_all(session)
		products = product_dao.get_all(session)

	product_count: dict[int, int] = {}
	for product in products:
		product_count[product.storage_location_id] = product_count.get(product.storage_location_id, 0) + 1

	rows: list[dict] = []
	for location in locations:
		rows.append(
			{
				"storage_location_id": location.storage_location_id,
				"name": location.name,
				"shelf_number": location.shelf_number or "-",
				"products": product_count.get(location.storage_location_id, 0),
			}
		)
	return rows


@ui.page("/locations")
def locations_page() -> None:
	def content() -> None:
		rows = _build_rows()

		with ui.card().classes("rounded-3xl p-6 shadow-sm"):
			ui.label("Storage Locations").classes("text-xl font-semibold text-gray-900")
			ui.label("Track shelves and product distribution.").classes("text-sm text-gray-500")
			ui.separator().classes("my-4")

			if not rows:
				ui.label("No storage locations found.").classes("text-base text-gray-500")
				return

			ui.table(
				columns=[
					{"name": "storage_location_id", "label": "ID", "field": "storage_location_id"},
					{"name": "name", "label": "Name", "field": "name"},
					{"name": "shelf_number", "label": "Shelf", "field": "shelf_number"},
					{"name": "products", "label": "Products", "field": "products"},
				],
				rows=rows,
				row_key="storage_location_id",
			).classes("w-full")

	render_shell("Locations", "Manage storage areas and shelf assignments.", "/locations", content)

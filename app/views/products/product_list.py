from nicegui import ui

from app.data_access.dao import CategoryDAO, ProductDAO, StorageLocationDAO
from app.data_access.db import engine, get_session
from app.services.product_services import ProductServices


def _build_rows() -> list[dict]:
	product_dao = ProductDAO(engine)
	category_dao = CategoryDAO(engine)
	location_dao = StorageLocationDAO(engine)
	product_service = ProductServices(product_dao, category_dao, location_dao)

	with get_session() as session:
		products = product_service.get_all_products(session)
		categories = {c.category_id: c.name for c in category_dao.get_all(session)}
		locations = {
			l.storage_location_id: l.name
			for l in location_dao.get_all(session)
		}

	rows: list[dict[str, object]] = []
	for p in products:
		rows.append(
			{
				"product_id": p.product_id,
				"name": p.name,
				"quantity": p.quantity,
				"minimum_stock": p.minimum_stock,
				"status": p.status,
				"category": categories.get(p.category_id, "-") if p.category_id else "-",
				"location": locations.get(p.storage_location_id, "-")
				if p.storage_location_id
				else "-",
			}
		)
	return rows


def render_product_list(container) -> None:
	container.clear()
	rows = _build_rows()

	with container:
		ui.label("Product List").classes("text-xl font-semibold text-gray-900")
		ui.label("Overview of all stored products.").classes("text-sm text-gray-500")
		ui.separator().classes("my-4")

		if not rows:
			ui.label("No products found.").classes("text-base text-gray-500")
			return

		columns = [
			{"name": "product_id", "label": "ID", "field": "product_id", "align": "left"},
			{"name": "name", "label": "Name", "field": "name", "align": "left"},
			{"name": "quantity", "label": "Qty", "field": "quantity", "align": "left"},
			{
				"name": "minimum_stock",
				"label": "Min Stock",
				"field": "minimum_stock",
				"align": "left",
			},
			{"name": "status", "label": "Status", "field": "status", "align": "left"},
			{"name": "category", "label": "Category", "field": "category", "align": "left"},
			{"name": "location", "label": "Location", "field": "location", "align": "left"},
		]

		ui.table(columns=columns, rows=rows, row_key="product_id").classes("w-full")

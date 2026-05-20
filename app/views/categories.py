from collections import Counter

from nicegui import ui

from app.data_access.db import engine, get_session
from app.data_access.dao import CategoryDAO, ProductDAO, StorageLocationDAO
from app.services.category_services import CategoryServices
from app.services.product_services import ProductServices

from .layout import render_shell


def _build_rows() -> list[dict]:
	category_dao = CategoryDAO(engine)
	product_dao = ProductDAO(engine)
	category_service = CategoryServices(category_dao, product_dao)
	product_service = ProductServices(product_dao, category_dao, StorageLocationDAO(engine))

	with get_session() as session:
		categories = category_service.get_all_categories(session)
		products = product_service.get_all_products(session)

	product_count = Counter(product.category_id for product in products)

	rows: list[dict] = []
	for category in categories:
		rows.append(
			{
				"category_id": category.category_id,
				"name": category.name,
				"type": category.type,
				"products": product_count.get(category.category_id, 0),
			}
		)
	return rows


@ui.page("/categories")
def categories_page() -> None:
	def content() -> None:
		rows = _build_rows()

		with ui.card().classes("rounded-3xl p-6 shadow-sm"):
			ui.label("Categories").classes("text-xl font-semibold text-gray-900")
			ui.label("Manage product groups and category types.").classes("text-sm text-gray-500")
			ui.separator().classes("my-4")

			if not rows:
				ui.label("No categories found.").classes("text-base text-gray-500")
				return

			ui.table(
				columns=[
					{"name": "category_id", "label": "ID", "field": "category_id"},
					{"name": "name", "label": "Name", "field": "name"},
					{"name": "type", "label": "Type", "field": "type"},
					{"name": "products", "label": "Products", "field": "products"},
				],
				rows=rows,
				row_key="category_id",
			).classes("w-full")

	render_shell("Categories", "Organize products by category and track usage.", "/categories", content)

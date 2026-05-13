from nicegui import ui

from app.data_access.dao import CategoryDAO, ProductDAO, StorageLocationDAO
from app.data_access.db import engine, get_session
from app.services.product_services import ProductServices


def _select_options() -> tuple[dict[int, str], dict[int, str]]:
	category_dao = CategoryDAO(engine)
	location_dao = StorageLocationDAO(engine)

	with get_session() as session:
		categories = {c.category_id: c.name for c in category_dao.get_all(session)}
		locations = {
			l.storage_location_id: l.name
			for l in location_dao.get_all(session)
		}
	return categories, locations


def render_add_product_form(on_created=None) -> None:
	categories, locations = _select_options()

	with ui.card().classes("w-full rounded-3xl p-6 shadow-sm"):
		ui.label("Add Product").classes("text-xl font-semibold text-gray-900")
		ui.label("Create a new product record.").classes("text-sm text-gray-500")
		ui.separator().classes("my-4")

		name = ui.input("Name").props("outlined")
		description = ui.input("Description").props("outlined")
		quantity = ui.number("Quantity", value=0, min=0).props("outlined")
		minimum_stock = ui.number("Minimum stock", value=0, min=0).props("outlined")
		status = ui.select(["active", "inactive"], value="active", label="Status").props("outlined")
		category_id = ui.select(categories, label="Category").props("outlined")
		location_id = ui.select(locations, label="Storage location").props("outlined")

		def create_product() -> None:
			product_name = str(name.value or "").strip()
			description_value = str(description.value or "").strip()

			if not product_name:
				ui.notify("Product name is required", type="negative")
				return

			if not category_id.value or not location_id.value:
				ui.notify("Category and location are required", type="negative")
				return
			if quantity.value < 0 or minimum_stock.value < 0:
				ui.notify("Quantity and minimum stock cannot be negative", type="negative")
				return
			if quantity.value < minimum_stock.value:
				ui.notify("Quantity cannot be less than minimum stock", type="negative")
				return

			product_data = {
				"name": product_name,
				"description": description_value or None,
				"quantity": int(quantity.value or 0),
				"minimum_stock": int(minimum_stock.value or 0),
				"status": status.value or "active",
				"category_id": int(category_id.value),
				"storage_location_id": int(location_id.value),
			}

			product_service = ProductServices(
				ProductDAO(engine),
				CategoryDAO(engine),
				StorageLocationDAO(engine),
			)

			try:
				with get_session() as session:
					product_service.create_product(session, product_data)
				ui.notify("Product created", type="positive")

				name.set_value("")
				description.set_value("")
				quantity.set_value(0)
				minimum_stock.set_value(0)
				status.set_value("active")
				category_id.set_value(None)
				location_id.set_value(None)

				if on_created:
					on_created()
			except ValueError as exc:
				ui.notify(str(exc), type="negative")

		ui.button("Create Product", on_click=create_product).props("color=primary no-caps")

from nicegui import ui

from app.data_access.dao import ProductDAO
from app.data_access.db import engine, get_session


def _load_dashboard_stats() -> dict:
	product_dao = ProductDAO(engine)
	with get_session() as session:
		products = product_dao.get_all(session)

	total_products = len(products)
	total_quantity = sum(p.quantity for p in products)
	low_stock = sum(1 for p in products if p.quantity <= p.minimum_stock)

	return {
		"total_products": total_products,
		"total_quantity": total_quantity,
		"low_stock": low_stock,
	}


@ui.page("/")
def dashboard_page() -> None:
	stats = _load_dashboard_stats()

	ui.label("Inventory Dashboard").classes("text-h4")
	ui.label("Quick overview of current stock status").classes("text-grey-7")

	with ui.row().classes("w-full q-col-gutter-md"):
		with ui.card().classes("col"):
			ui.label("Products").classes("text-subtitle2 text-grey-7")
			ui.label(str(stats["total_products"])).classes("text-h5")

		with ui.card().classes("col"):
			ui.label("Total Quantity").classes("text-subtitle2 text-grey-7")
			ui.label(str(stats["total_quantity"])).classes("text-h5")

		with ui.card().classes("col"):
			ui.label("Low Stock").classes("text-subtitle2 text-grey-7")
			ui.label(str(stats["low_stock"])).classes("text-h5 text-red-6")

	if stats["low_stock"] > 0:
		ui.notification(
			f"{stats['low_stock']} product(s) are at or below minimum stock.",
			type="warning",
			timeout=3000,
		)


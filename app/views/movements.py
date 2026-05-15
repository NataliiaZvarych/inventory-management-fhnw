from nicegui import ui

from app.data_access.db import engine, get_session
from app.data_access.dao import CategoryDAO, ProductDAO, StockMovementDAO, StorageLocationDAO, UserDAO
from app.services.movement_services import MovementService
from app.services.product_services import ProductServices
from app.services.user_service import UserService

from .layout import render_shell


def _build_rows() -> list[dict]:
	product_dao = ProductDAO(engine)
	user_dao = UserDAO(engine)
	movement_service = MovementService(product_dao, user_dao, StockMovementDAO(engine), StorageLocationDAO(engine))
	product_service = ProductServices(product_dao, CategoryDAO(engine), StorageLocationDAO(engine))
	user_service = UserService(user_dao)

	with get_session() as session:
		movements = movement_service.get_all_movements(session)
		products = {product.product_id: product.name for product in product_service.get_all_products(session)}
		users = {user.user_id: user.name for user in user_service.get_all_users(session)}

	rows: list[dict] = []
	for movement in sorted(movements, key=lambda item: item.timestamp, reverse=True):
		rows.append(
			{
				"movement_id": movement.movement_id,
				"product": products.get(movement.product_id, "-"),
				"user": users.get(movement.user_id, "-"),
				"quantity": movement.quantity,
				"movement_type": movement.movement_type,
				"timestamp": movement.timestamp.strftime("%d.%m.%Y %H:%M") if movement.timestamp else "-",
				"note": movement.note or "-",
			}
		)
	return rows


@ui.page("/movements")
def movements_page() -> None:
	def content() -> None:
		rows = _build_rows()

		with ui.card().classes("w-full rounded-3xl p-6 shadow-sm"):
			ui.label("Movements").classes("text-xl font-semibold text-gray-900")
			ui.label("Review stock changes and activity history.").classes("text-sm text-gray-500")
			ui.separator().classes("my-4")

			if not rows:
				ui.label("No movements recorded yet.").classes("text-base text-gray-500")
				return

			ui.table(
				columns=[
					{"name": "movement_id", "label": "ID", "field": "movement_id"},
					{"name": "product", "label": "Product", "field": "product"},
					{"name": "user", "label": "User", "field": "user"},
					{"name": "quantity", "label": "Qty", "field": "quantity"},
					{"name": "movement_type", "label": "Type", "field": "movement_type"},
					{"name": "timestamp", "label": "Date", "field": "timestamp"},
					{"name": "note", "label": "Note", "field": "note"},
				],
				rows=rows,
				row_key="movement_id",
			).classes("w-full")

	render_shell("Movements", "Track stock changes and movement history.", "/movements", content)

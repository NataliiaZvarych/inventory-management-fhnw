from nicegui import ui

from app.data_access.dao import CategoryDAO, ProductDAO, StockMovementDAO, StorageLocationDAO, UserDAO
from app.data_access.db import engine, get_session

from .layout import render_shell


def _load_dashboard_data() -> dict:
	product_dao = ProductDAO(engine)
	category_dao = CategoryDAO(engine)
	location_dao = StorageLocationDAO(engine)
	user_dao = UserDAO(engine)
	movement_dao = StockMovementDAO(engine)

	with get_session() as session:
		products = product_dao.get_all(session)
		categories = category_dao.get_all(session)
		locations = location_dao.get_all(session)
		users = user_dao.get_all(session)
		movements = movement_dao.get_all(session)
		product_names = {product.product_id: product.name for product in products}
		user_names = {user.user_id: user.name for user in users}

	low_stock_products = [product for product in products if product.quantity <= product.minimum_stock]
	recent_movements = sorted(movements, key=lambda item: item.timestamp, reverse=True)[:5]

	return {
		"total_products": len(products),
		"total_quantity": sum(product.quantity for product in products),
		"low_stock": len(low_stock_products),
		"total_movements": len(movements),
		"categories": len(categories),
		"locations": len(locations),
		"users": len(users),
		"low_stock_products": low_stock_products,
		"recent_movements": [
			{
				"movement_id": movement.movement_id,
				"product": product_names.get(movement.product_id, "-"),
				"user": user_names.get(movement.user_id, "-"),
				"quantity": movement.quantity,
				"movement_type": movement.movement_type,
				"timestamp": movement.timestamp.strftime("%d.%m.%Y %H:%M") if movement.timestamp else "-",
			}
			for movement in recent_movements
		],
	}


def _stat_card(title: str, value: str, icon: str, accent: str) -> None:
	with ui.card().classes("flex-1 rounded-3xl p-5 shadow-sm"):
		with ui.row().classes("items-center justify-between"):
			with ui.column().classes("gap-1"):
				ui.label(title).classes("text-sm text-gray-500")
				ui.label(value).classes("text-3xl font-bold text-gray-900")
			ui.icon(icon).classes(f"text-3xl {accent}")


@ui.page("/dashboard")
def dashboard_page() -> None:
	data = _load_dashboard_data()

	def content() -> None:
		with ui.row().classes("w-full gap-4 flex-wrap"):
			_stat_card("Products", str(data["total_products"]), "inventory_2", "text-[#6fa1d8]")
			_stat_card("Total Stock", str(data["total_quantity"]), "stacked_line_chart", "text-[#6fa1d8]")
			_stat_card("Low Stock", str(data["low_stock"]), "warning", "text-amber-500")
			_stat_card("Movements", str(data["total_movements"]), "swap_horiz", "text-[#6fa1d8]")

		with ui.row().classes("w-full gap-6 flex-wrap items-start"):
			with ui.card().classes("flex-1 min-w-[320px] rounded-3xl p-6 shadow-sm"):
				ui.label("Low stock").classes("text-xl font-semibold text-gray-900")
				ui.label("Products that need attention now.").classes("text-sm text-gray-500")
				ui.separator().classes("my-4")

				if not data["low_stock_products"]:
					ui.label("No low stock items right now.").classes("text-base text-gray-500")
				else:
					for product in data["low_stock_products"]:
						with ui.card().classes("mb-3 w-full rounded-2xl bg-[#fff7e8] p-4 shadow-none"):
							with ui.row().classes("items-center justify-between"):
								with ui.column().classes("gap-0"):
									ui.label(product.name).classes("text-base font-semibold text-gray-900")
									ui.label(f"Minimum: {product.minimum_stock}").classes("text-xs text-gray-500")
								ui.label(str(product.quantity)).classes("text-2xl font-bold text-amber-600")

				with ui.card().classes("flex-1 min-w-[320px] rounded-3xl p-6 shadow-sm"):
					ui.label("Recent movements").classes("text-xl font-semibold text-gray-900")
					ui.label("Latest inventory activity.").classes("text-sm text-gray-500")
					ui.separator().classes("my-4")

					if not data["recent_movements"]:
						ui.label("No movements yet.").classes("text-base text-gray-500")
					else:
						for movement in data["recent_movements"]:
							with ui.card().classes("mb-3 w-full rounded-2xl bg-white p-4 shadow-none ring-1 ring-gray-100"):
								with ui.row().classes("items-center justify-between"):
									with ui.column().classes("gap-0"):
										ui.label(movement["product"]).classes("text-base font-semibold text-gray-900")
										ui.label(f"{movement['user']} • {movement['timestamp']}").classes("text-xs text-gray-500")
									ui.label(f"{movement['movement_type']} · {movement['quantity']}").classes("text-sm font-semibold text-[#2f6fb1]")

		with ui.row().classes("w-full gap-4 flex-wrap"):
			with ui.card().classes("flex-1 rounded-3xl p-5 shadow-sm"):
				ui.label("Quick actions").classes("text-lg font-semibold text-gray-900")
				ui.label("Jump to the most used sections.").classes("text-sm text-gray-500")
				ui.separator().classes("my-4")
				with ui.row().classes("gap-3 flex-wrap"):
					ui.button("Products", on_click=lambda: ui.navigate.to("/products")).props("color=primary no-caps")
					ui.button("Categories", on_click=lambda: ui.navigate.to("/categories")).props("outline no-caps")
					ui.button("Movements", on_click=lambda: ui.navigate.to("/movements")).props("outline no-caps")

			with ui.card().classes("flex-1 rounded-3xl p-5 shadow-sm"):
				ui.label("Overview").classes("text-lg font-semibold text-gray-900")
				ui.label("Data in the current demo database.").classes("text-sm text-gray-500")
				ui.separator().classes("my-4")
				with ui.column().classes("gap-3"):
					ui.label(f"Categories: {data['categories']}").classes("text-base text-gray-700")
					ui.label(f"Locations: {data['locations']}").classes("text-base text-gray-700")
					ui.label(f"Users: {data['users']}").classes("text-base text-gray-700")

	render_shell("Dashboard", "Quick overview of stock status and activity.", "/dashboard", content)



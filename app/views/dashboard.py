from nicegui import ui
from app.data_access.db import engine, get_session
from app.services import *
from app.data_access.dao import *
from .layout import render_shell
from app.views.auth_state import current_user


def _load_dashboard_data() -> dict:
	product_service = ProductServices(ProductDAO(engine), CategoryDAO(engine), StorageLocationDAO(engine))
	category_service = CategoryServices(CategoryDAO(engine), ProductDAO(engine))
	location_service = LocationServices(StorageLocationDAO(engine))
	user_service = UserService(UserDAO(engine))
	movement_service = MovementService(ProductDAO(engine), UserDAO(engine), StockMovementDAO(engine), StorageLocationDAO(engine))

	with get_session() as session:
		products = product_service.get_all_products(session)
		categories = category_service.get_all_categories(session)
		locations = location_service.get_all_storage_locations(session)
		users = user_service.get_all_users(session)
		movements = movement_service.get_all_movements(session)
		product_names = {product.product_id: product.name for product in products}
		user_names = {user.user_id: user.name for user in users}

	low_stock_products = [
    product for product in products
    if product.quantity <= product.minimum_stock][:5]
	recent_movements = sorted(movements, key=lambda item: item.timestamp, reverse=True)[:5]
	
	category_names = {
	category.category_id: category.name
	for category in categories
	}

	category_count = {}

	for product in products:
		category_name = category_names.get(product.category_id, "Unknown")
		category_count[category_name] = category_count.get(category_name, 0) + 1

	category_chart_data = [
		{
			"name": category_name,
			"value": count,
		}
		for category_name, count in category_count.items()
	]
	


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
		"category_chart_data": category_chart_data,
	}


def _stat_card(title: str, value: str, icon: str, icon_color: str):
    with ui.card().classes(
        "rounded-2xl shadow-sm p-3 bg-white min-w-[160px] flex-1"
    ):
        with ui.row().classes("items-center gap-2"):

            ui.icon(icon).classes(
                f"text-2xl {icon_color}"
            )

            with ui.column().classes("gap-0"):

                ui.label(value).classes(
                    "text-xl font-bold text-[#0f172a] leading-none"
                )

                ui.label(title).classes(
                    "text-xs text-[#667085]"
                )


@ui.page("/dashboard")
def dashboard_page() -> None:
	data = _load_dashboard_data()

	def content() -> None:
		with ui.row().classes("w-full gap-4 flex-wrap"):
			_stat_card("Total Products", str(data["total_products"]), "inventory_2", "text-[#6fa1d8]")
			_stat_card("Total Units", str(data["total_quantity"]), "stacked_line_chart", "text-[#6fa1d8]")
			_stat_card("Low Stock", str(data["low_stock"]), "warning", "text-amber-500")
			_stat_card("Movements", str(data["total_movements"]), "swap_horiz", "text-[#6fa1d8]")
			_stat_card("Categories", str(data["categories"]), "category", "text-[#6fa1d8]")
			_stat_card("Locations", str(data["locations"]), "location_on", "text-[#6fa1d8]")
			_stat_card("Users", str(data["users"]), "group", "text-[#6fa1d8]")

		with ui.row().classes("w-full gap-6 flex-wrap items-start"):
			with ui.card().classes("flex-1 min-w-[320px] rounded-2xl p-3 shadow-sm max-h-[320px] min-h-[320px] overflow-y-auto"):
				with ui.column().classes("gap-0 mb-1"):
					ui.label("Low stock").classes("text-xl font-semibold text-gray-900 leading-tight" )
					ui.label("Showing 5 most critical items").classes("text-sm text-gray-500 leading-tight")
				ui.separator().classes("my-1")

				if not data["low_stock_products"]:
					ui.label("No low stock items right now.").classes("text-base text-gray-500")
				else:
					for product in data["low_stock_products"]:
						with ui.card().classes("mb-2 w-full rounded-xl bg-[#fff7e8] p-3 shadow-none"):
							with ui.row().classes("items-center justify-between"):
								with ui.column().classes("gap-0"):
									ui.label(product.name).classes("text-base font-semibold text-gray-900 leading-tight")
									ui.label(f"Minimum: {product.minimum_stock}").classes("text-xs text-gray-500")
								ui.label(str(product.quantity)).classes("text-xl font-bold text-amber-600")
			with ui.card().classes("flex-1 min-w-[320px] rounded-2xl p-3 shadow-sm max-h-[320px] min-h-[320px] overflow-y-auto"):
				with ui.column().classes("gap-0 mb-1"):
					ui.label("Recent movements").classes("text-xl font-semibold text-gray-900 leading-tight")
					ui.label("Latest inventory activity.").classes("text-sm text-gray-500 leading-tight")
				ui.separator().classes("my-1")

				if not data["recent_movements"]:
					ui.label("No movements yet.").classes("text-base text-gray-500")
				else:
					for movement in data["recent_movements"]:
						with ui.card().classes("mb-2 w-full rounded-2xl bg-[#fff7e8] p-3 shadow-none ring-1 ring-gray-100"):
							with ui.row().classes("items-center justify-between"):
								with ui.column().classes("gap-0"):
									ui.label(movement["product"]).classes("text-base font-semibold text-gray-900")
									ui.label(f"{movement['user']} • {movement['timestamp']}").classes("text-xs text-gray-500")
								ui.label(f"{movement['movement_type']} · {movement['quantity']}").classes("text-sm font-semibold text-[#2f6fb1]")

			with ui.row().classes("w-full gap-6 flex-wrap items-start"):
				with ui.card().classes(
					"flex-1 min-w-[420px] rounded-3xl p-6 shadow-sm"
				):
					ui.label("Products by Category").classes(
						"text-xl font-semibold text-gray-900 mb-4"
					)

					if not data["category_chart_data"]:
						ui.label("No products available for chart.").classes("text-gray-500")
					else:
						ui.echart({
							"tooltip": {
								"trigger": "item",
								"formatter": "{b}: {c} products ({d}%)"
							},
							"legend": {
								"orient": "vertical",
								"right": "5%",
								"top": "center"
							},
							"series": [
								{
									"name": "Products by Category",
									"type": "pie",

									# donut style
									"radius": ["50%", "72%"],

									# move chart slightly left
									"center": ["35%", "50%"],

									"data": data["category_chart_data"],

									# hide labels around chart
									"label": {
											"show": True,
											"position": "outside",
											"formatter": "{d}%",
											"fontSize": 14,
											"fontWeight": "bold",
											"color": "#374151"
									},

									"labelLine": {
										"show": True
									},

									"emphasis": {
										"itemStyle": {
											"shadowBlur": 10,
											"shadowOffsetX": 0,
											"shadowColor": "rgba(0, 0, 0, 0.3)"
										}
									}
								}
							]
						}).classes("w-full h-80")

				with ui.card().classes(
					"flex-1 min-w-[420px] rounded-3xl p-6 shadow-sm"
				):

					ui.label("Stock by Location").classes(
						"text-xl font-semibold text-gray-900"
					)

					ui.echart({
						"tooltip": {},
						"xAxis": {
							"type": "category",
							"data": ["Shelf A", "Shelf B", "Shelf C", "Shelf D"]
						},
						"yAxis": {
							"type": "value"
						},
						"series": [{
							"type": "bar",
							"data": [25, 40, 15, 35]
						}]
					}).classes("w-full h-80")	




	render_shell(
    title="Dashboard",
    subtitle="Overview of inventory",
    active_route="/dashboard",
    content_builder=content
)
 

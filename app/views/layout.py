from collections.abc import Callable

from nicegui import ui


NAV_ITEMS = [
	{"label": "Dashboard", "route": "/dashboard", "icon": "dashboard"},
	{"label": "Products", "route": "/products", "icon": "inventory_2"},
	{"label": "Categories", "route": "/categories", "icon": "category"},
	{"label": "Locations", "route": "/locations", "icon": "location_on"},
	{"label": "Movements", "route": "/movements", "icon": "swap_horiz"},
	{"label": "Users", "route": "/users", "icon": "group"},
]


def render_shell(
	title: str,
	subtitle: str,
	active_route: str,
	content_builder: Callable[[], None],
) -> None:
	with ui.row().classes("w-full min-h-screen gap-0 bg-[#f5f7fb]"):
		with ui.card().classes(
			"w-72 min-h-screen rounded-none border-r border-gray-200 bg-white shadow-none"
		):
			with ui.column().classes("h-full justify-between p-6 gap-6"):
				with ui.column().classes("gap-6"):
					with ui.row().classes("items-center gap-3"):
						ui.label("📦").classes("text-4xl")
						with ui.column().classes("gap-0"):
							ui.label("Lagerverwaltung").classes("text-2xl font-bold text-gray-900")
							ui.label("Inventarsystem").classes("text-sm text-gray-500")

					with ui.column().classes("gap-2"):
						for item in NAV_ITEMS:
							button = ui.button(
								item["label"],
								icon=item["icon"],
								on_click=lambda route=item["route"]: ui.navigate.to(route),
							).props("flat no-caps align=left")
							button.classes("w-full justify-start rounded-2xl px-4 py-3")
							if item["route"] == active_route:
								button.classes("bg-[#e8f1ff] text-[#2f6fb1]")
							else:
								button.classes("text-gray-700")

					ui.separator()

					with ui.column().classes("gap-3 rounded-2xl bg-[#f8fafc] p-4"):
						ui.label("Quick access").classes("text-sm font-semibold text-gray-700")
						ui.button("Go to Products", on_click=lambda: ui.navigate.to("/products")).props(
							"flat no-caps color=primary"
						)
						ui.button("Open Dashboard", on_click=lambda: ui.navigate.to("/dashboard")).props(
							"flat no-caps outline"
						)

		with ui.column().classes("flex-1 gap-6 p-6"):
			with ui.row().classes("items-start justify-between gap-4"):
				with ui.column().classes("gap-1"):
					ui.label(title).classes("text-4xl font-bold text-gray-900")
					ui.label(subtitle).classes("text-base text-gray-500")

				with ui.card().classes("rounded-2xl bg-white px-4 py-3 shadow-sm"):
					with ui.row().classes("items-center gap-3"):
						ui.label("N").classes(
								"flex h-10 w-10 items-center justify-center rounded-full bg-[#e8f1ff] text-sm font-bold text-[#2f6fb1]"
							)
						with ui.column().classes("gap-0"):
								ui.label("Natalia").classes("text-sm font-semibold text-gray-900")
								ui.label("admin").classes("text-xs text-gray-500")

			content_builder()

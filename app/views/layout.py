from collections.abc import Callable
from nicegui import ui
from app.views.auth_state import current_user as auth_current_user

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
	current_user: dict = None,
) -> None:
	if current_user is None:
		current_user = auth_current_user

	def logout() -> None:
		auth_current_user["user_id"] = None
		auth_current_user["name"] = None
		auth_current_user["role"] = None
		ui.navigate.to("/")

	def open_profile() -> None:
		with ui.dialog() as dialog, ui.card().classes("w-80 rounded-xl p-5"):
			ui.label("Profile").classes("text-xl font-bold text-gray-900")
			ui.separator()
			with ui.column().classes("gap-2 mt-2"):
				ui.label(f"👤 Name: {current_user.get('name', 'User')}")
				ui.label(f"🛡 Role: {current_user.get('role', '-')}")
				ui.label(f"🆔 User ID: {current_user.get('user_id', '-')}")
			ui.button("Close", on_click=dialog.close).props("flat") .classes("mt-4 self-end")
		dialog.open()	
	def open_settings() -> None:
		with ui.dialog() as dialog, ui.card().classes("w-80 rounded-xl p-5"):
			ui.label("Settings").classes("text-xl font-bold text-gray-500")
			ui.separator()

			with ui.column().classes("gap-2 mt-2"):
				ui.label("🎨 Theme: Light mode")
				ui.label("🌐 Language: English")
				ui.label("🔔 Notifications: Enabled")

			
			ui.button("Close", on_click=dialog.close).props("flat") .classes("mt-4 self-end")
		dialog.open()

	with ui.row().classes("w-full min-h-screen gap-0 bg-[#f5f7fb] flex-nowrap"):
		with ui.card().classes(
			"w-72 min-w-72 min-h-screen shrink-0 rounded-none border-r border-gray-200 bg-white shadow-none"
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



		with ui.column().classes("flex-1 min-w-0 gap-4 p-4"):
			with ui.row().classes("w-full items-start justify-between gap-4"):
				with ui.column().classes("gap-1"):
					ui.label(title).classes("text-4xl font-bold text-gray-900")
					ui.label(subtitle).classes("text-base text-gray-500")

				user_name = (
					current_user["name"] if current_user and current_user.get("name") 
					else "User"
				)
				user_role = (
					current_user["role"] if current_user and current_user.get("role") 
					else "User"
				)

				with ui.button().props("flat no-caps").classes("" \
					"ml-auto rounded-2xl bg-white px-3 py-3 shadow-sm "
					"border border-gray-100 hover:bg-[#f8fafc] hover:shadow-md"
					"transition-all duration-200"
				):

												   
					with ui.row().classes("items-center gap-2 no-wrap"):											 					
						ui.label(user_name[0].upper()).classes(
							"flex h-8 w-8 items-center justify-center "
							"rounded-full bg-[#e8f1ff] text-sm "
							"font-bold text-[#2f6fb1]"
						)

						with ui.column().classes("gap-0 items-start"):
							ui.label(user_name).classes(
								"text-sm font-semibold text-gray-900 leading-none"
							)

							ui.label(user_role).classes(
								"text-xs text-gray-500"
							)
						ui.icon("keyboard_arrow_down").classes("text-gray-400 text-xs")

					with ui.menu().classes("rounded-xl shadow-lg"):
						ui.menu_item("Profile", on_click=open_profile)
						ui.menu_item("Settings", on_click=open_settings)
						ui.separator()
						ui.menu_item("Logout", on_click=logout)

			content_builder()

from nicegui import ui


@ui.page("/")
def login_page() -> None:
	with ui.column().classes(
		"w-full min-h-screen items-center justify-center bg-[#f5f7fb] px-6"
	):
		with ui.card().classes("w-full max-w-md rounded-3xl p-8 shadow-xl"):
			with ui.column().classes("gap-6"):
				with ui.row().classes("items-center gap-4"):
					ui.label("📦").classes("text-4xl")
					with ui.column().classes("gap-0"):
						ui.label("Lagerverwaltung").classes("text-3xl font-bold text-gray-900")
						ui.label("Inventarsystem").classes("text-base text-gray-500")

				ui.separator()

				username = ui.input("Username or User ID", value="Natalia").props("outlined")
				password = ui.input(
					"Password optional",
					password=True,
					password_toggle_button=True,
				).props("outlined")

				def login() -> None:
					ui.notify(f"Welcome, {username.value or 'user'}", type="positive")
					ui.navigate.to("/dashboard")

				ui.button("LOGIN", on_click=login).props("color=primary").classes("w-full")

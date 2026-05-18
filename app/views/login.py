from nicegui import ui

from app.data_access.dao import UserDAO
from app.data_access.db import engine, get_session


@ui.page("/login")
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

				username = ui.input(
					"Username or User ID",
					 value="Natalia",
				).props("outlined") .on("keydown.enter", lambda _: login())
				password = ui.input(
					"Password optional",
					password=True,
					password_toggle_button=True,
				).props("outlined").on("keydown.enter", lambda _: login())

				def login() -> None:
					user_dao = UserDAO(engine)
					try:
						with get_session() as session:
							login_name = str(username.value or "").strip()
							users = user_dao.get_all(session)
							user = next((item for item in users if item.name == login_name), None)
							if not user:
								raise ValueError("User not found")
							if password.value:
								import hashlib

								password_hash = hashlib.sha256(str(password.value).encode()).hexdigest()
								if user.password_hash != password_hash:
									raise ValueError("Incorrect password")

						ui.notify(f"Welcome, {user.name if user else username.value or 'user'}", type="positive")
						ui.navigate.to("/dashboard")
					except ValueError as exc:
						ui.notify(str(exc), type="negative")

				ui.button("LOGIN", on_click=login).props("color=primary").classes("w-full")

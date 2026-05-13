from collections import Counter

from nicegui import ui

from app.data_access.dao import StockMovementDAO, UserDAO
from app.data_access.db import engine, get_session

from .layout import render_shell


def _build_rows() -> list[dict]:
	user_dao = UserDAO(engine)
	movement_dao = StockMovementDAO(engine)

	with get_session() as session:
		users = user_dao.get_all(session)
		movements = movement_dao.get_all(session)

	movement_count = Counter(movement.user_id for movement in movements)

	rows: list[dict] = []
	for user in users:
		rows.append(
			{
				"user_id": user.user_id,
				"name": user.name,
				"role": user.role,
				"movements": movement_count.get(user.user_id, 0),
			}
		)
	return rows


@ui.page("/users")
def users_page() -> None:
	def content() -> None:
		rows = _build_rows()

		with ui.card().classes("rounded-3xl p-6 shadow-sm"):
			ui.label("Users").classes("text-xl font-semibold text-gray-900")
			ui.label("Monitor demo users and their activity.").classes("text-sm text-gray-500")
			ui.separator().classes("my-4")

			if not rows:
				ui.label("No users found.").classes("text-base text-gray-500")
				return

			ui.table(
				columns=[
					{"name": "user_id", "label": "ID", "field": "user_id"},
					{"name": "name", "label": "Name", "field": "name"},
					{"name": "role", "label": "Role", "field": "role"},
					{"name": "movements", "label": "Movements", "field": "movements"},
				],
				rows=rows,
				row_key="user_id",
			).classes("w-full")

	render_shell("Users", "View application users and usage counts.", "/users", content)

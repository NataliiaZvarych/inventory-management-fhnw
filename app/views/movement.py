import sys
from pathlib import Path
from typing import Callable, Optional

from nicegui import ui

# Allow direct execution of this file (e.g. on macOS) by exposing app/ on sys.path.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.inventory_service import InventoryService


def render_movement_controls(on_inventory_changed: Optional[Callable[[], None]] = None) -> None:
	with ui.card().classes("w-full"):
		ui.label("Stock Movement").classes("text-lg font-semibold")

		product_id_input = ui.number("Product ID", value=1, min=1).classes("w-full")
		user_id_input = ui.number("User ID", value=1, min=1).classes("w-full")
		amount_input = ui.number("Amount", value=1, min=1).classes("w-full")
		movement_type = ui.select(["in", "out"], value="in", label="Type").classes("w-full")
		feedback = ui.label("").classes("text-sm")

		def apply_movement() -> None:
			product_id = int(product_id_input.value or 0)
			user_id = int(user_id_input.value or 0)
			amount = int(amount_input.value or 0)

			if movement_type.value == "in":
				result = InventoryService.receive_stock(product_id, user_id, amount)
			else:
				result = InventoryService.issue_stock(product_id, user_id, amount)

			if result is None:
				feedback.set_text("Movement failed. Check IDs and amount.")
				feedback.classes("text-red-600", remove="text-green-600")
				return

			feedback.set_text("Movement applied")
			feedback.classes("text-green-600", remove="text-red-600")

			if on_inventory_changed:
				on_inventory_changed()

		ui.button("Apply", on_click=apply_movement).classes("w-full")


if __name__ == "__main__":
	print("Run the app from app/main.py, not from an individual view file.")

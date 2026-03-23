from typing import Callable, Optional

from nicegui import ui

from services.product_service import ProductService


def render_add_product(on_product_added: Optional[Callable[[], None]] = None) -> None:
	with ui.card().classes("w-full"):
		ui.label("Add Product").classes("text-lg font-semibold")

		name_input = ui.input("Name").classes("w-full")
		quantity_input = ui.number("Quantity", value=0, min=0).classes("w-full")
		min_quantity_input = ui.number("Min Quantity", value=5, min=0).classes("w-full")
		status_input = ui.select(
			["available", "low_stock", "out_of_stock"],
			value="available",
			label="Status",
		).classes("w-full")

		feedback = ui.label("").classes("text-sm")

		def submit() -> None:
			if not name_input.value or not str(name_input.value).strip():
				feedback.set_text("Name is required")
				feedback.classes("text-red-600", remove="text-green-600")
				return

			ProductService.create_product(
				name=str(name_input.value).strip(),
				quantity=int(quantity_input.value or 0),
				min_quantity=int(min_quantity_input.value or 0),
				status=str(status_input.value or "available"),
			)

			feedback.set_text("Product created")
			feedback.classes("text-green-600", remove="text-red-600")
			name_input.value = ""
			quantity_input.value = 0
			min_quantity_input.value = 5
			status_input.value = "available"

			if on_product_added:
				on_product_added()

		ui.button("Add", on_click=submit).classes("w-full")

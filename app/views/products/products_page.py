from nicegui import ui

from app.views.products.add_product import render_add_product_form
from app.views.products.product_list import render_product_list

from ..layout import render_shell


@ui.page("/products")
def products_page() -> None:
	def content() -> None:
		with ui.row().classes("w-full gap-6 items-start flex-wrap"):
			with ui.column().classes("flex-1 min-w-[420px] gap-4"):
				with ui.card().classes("rounded-3xl p-6 shadow-sm"):
					ui.label("Products").classes("text-xl font-semibold text-gray-900")
					ui.label("Browse, create, and review product records.").classes("text-sm text-gray-500")
					ui.separator().classes("my-4")

					list_panel = ui.column().classes("w-full")

					def refresh_list() -> None:
						list_panel.clear()
						render_product_list(list_panel)

					refresh_list()

			with ui.column().classes("flex-1 min-w-[360px]"):
				render_add_product_form(on_created=refresh_list)

	render_shell("Products", "Manage your product catalog from one place.", "/products", content)

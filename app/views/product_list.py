from nicegui import ui

from services.product_service import ProductService


class ProductListView:
	def __init__(self) -> None:
		self.container = ui.column().classes("w-full")
		self.refresh()

	def refresh(self) -> None:
		self.container.clear()
		products = ProductService.list_products()

		with self.container:
			if not products:
				ui.label("No products yet").classes("text-gray-500")
				return

			columns = [
				{"name": "id", "label": "ID", "field": "id", "align": "left"},
				{"name": "name", "label": "Name", "field": "name", "align": "left"},
				{"name": "quantity", "label": "Quantity", "field": "quantity", "align": "left"},
				{
					"name": "min_quantity",
					"label": "Min Qty",
					"field": "min_quantity",
					"align": "left",
				},
				{"name": "status", "label": "Status", "field": "status", "align": "left"},
			]
			rows = [
				{
					"id": product.id,
					"name": product.name,
					"quantity": product.quantity,
					"min_quantity": product.min_quantity,
					"status": product.status,
				}
				for product in products
			]

			ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")

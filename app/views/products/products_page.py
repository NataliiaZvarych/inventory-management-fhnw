from nicegui import ui

from app.data_access.db import engine, get_session
from app.data_access.dao import ProductDAO, CategoryDAO, StorageLocationDAO
from app.services.product_services import ProductServices

from ..layout import render_shell


def _build_rows() -> list[dict]:
    product_dao = ProductDAO(engine)
    category_dao = CategoryDAO(engine)
    location_dao = StorageLocationDAO(engine)
    product_service = ProductServices(product_dao, category_dao, location_dao)

    with get_session() as session:
        products = product_service.get_all_products(session)

        rows: list[dict] = []
        for product in products:
            category = category_dao.get(session, product.category_id)
            location = location_dao.get(session, product.storage_location_id)
            rows.append(
                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "category": category.name if category else "-",
                    "storage_location": location.name if location else "-",
                    "quantity": product.quantity,
                    "minimum_stock": product.minimum_stock,
                    "status": product.status,
                }
            )

    return rows


@ui.page("/products")
def products_page() -> None:
    def content() -> None:
        rows = _build_rows()

        with ui.card().classes("w-full ounded-3xl p-6 shadow-sm"):
            with ui.column().classes("w-fullitems-center justify-between"):
                ui.label("Products").classes("text-xl font-semibold text-gray-900")
                ui.label("Browse and manage your inventory items.").classes("text-gray-500"
                )
                
            ui.separator().classes("my-4")

            if not rows:
                ui.label("No products found.").classes("text-base text-gray-500")
                return

            ui.table(
                columns=[
                    {"name": "product_id", "label": "ID", "field": "product_id"},
                    {"name": "name", "label": "Name", "field": "name"},
                    {"name": "category", "label": "Category", "field": "category"},
                    {"name": "storage_location", "label": "Location", "field": "storage_location"},
                    {"name": "quantity", "label": "Quantity", "field": "quantity"},
                    {"name": "minimum_stock", "label": "Min stock", "field": "minimum_stock"},
                    {"name": "status", "label": "Status", "field": "status"},
                ],
                rows=rows,
                row_key="product_id",
            ).classes("w-full")

    render_shell("Products", "Inventory items and their details.", "/products", content)

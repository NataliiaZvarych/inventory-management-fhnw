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

        def delete_row(row: dict) -> None:
            product_dao = ProductDAO(engine)
            category_dao = CategoryDAO(engine)
            location_dao = StorageLocationDAO(engine)
            product_service = ProductServices(product_dao, category_dao, location_dao)

            try:
                with get_session() as session:
                    product_service.delete_product(session, row["product_id"])

                ui.notify("Product deleted successfully", type="positive")
                ui.navigate.reload()

            except ValueError as error:
                ui.notify(str(error), type="negative")

        def edit_row(row: dict) -> None:
            with ui.dialog() as dialog, ui.card().classes("w-96"):
                ui.label(f"Edit product: {row['name']}").classes("text-lg font-semibold")

                name = ui.input("Name", value=row["name"]).classes("w-full")
                quantity = ui.number("Quantity", value=row["quantity"]).classes("w-full")
                minimum_stock = ui.number("Min stock", value=row["minimum_stock"]).classes("w-full")
                status = ui.input("Status", value=row["status"]).classes("w-full")

                def save_changes() -> None:
                    product_dao = ProductDAO(engine)
                    category_dao = CategoryDAO(engine)
                    location_dao = StorageLocationDAO(engine)
                    product_service = ProductServices(product_dao, category_dao, location_dao)

                    data = {
                        "name": name.value,
                        "quantity": int(quantity.value),
                        "minimum_stock": int(minimum_stock.value),
                        "status": status.value,
                    }

                    try:
                        with get_session() as session:
                            product_service.update_product(session, row["product_id"], data)

                        ui.notify("Product updated successfully", type="positive")
                        dialog.close()
                        ui.navigate.reload()

                    except ValueError as error:
                        ui.notify(str(error), type="negative")

                with ui.row().classes("justify-end w-full"):
                    ui.button("Cancel", on_click=dialog.close)
                    ui.button("Save", color="primary", on_click=save_changes)

            dialog.open()

        with ui.card().classes("w-full ounded-3xl p-6 shadow-sm"):
            with ui.column().classes("w-full items-center justify-between"):
                ui.label("Products").classes("text-xl font-semibold text-gray-900")
                ui.label("Browse and manage your inventory items.").classes("text-gray-500"
                )
                
            ui.separator().classes("my-4")

            if not rows:
                ui.label("No products found.").classes("text-base text-gray-500")
                return

            table = ui.table(
                columns=[
                    {"name": "product_id", "label": "ID", "field": "product_id"},
                    {"name": "name", "label": "Name", "field": "name"},
                    {"name": "category", "label": "Category", "field": "category"},
                    {"name": "storage_location", "label": "Location", "field": "storage_location"},
                    {"name": "quantity", "label": "Quantity", "field": "quantity"},
                    {"name": "minimum_stock", "label": "Min stock", "field": "minimum_stock"},
                    {"name": "status", "label": "Status", "field": "status"},
                    {"name": "actions", "label": "Actions", "field": "actions"},
                ],
                rows=rows,
                row_key="product_id",
            ).classes("w-full")

            table.add_slot(
                "body-cell-actions",
                """
<q-td :props="props">
    <q-btn dense flat color="primary" icon="edit" label="Bearbeiten"
            @click="$parent.$emit('edit', props.row)" />
    <q-btn dense flat color="negative" icon="delete" label="Löschen"
            @click="$parent.$emit('delete', props.row)" />
</q-td>
""",
            )
            table.on("delete", lambda e: delete_row(e.args))
            table.on("edit", lambda e: edit_row(e.args))

    render_shell("Products", "Inventory items and their details.", "/products", content)

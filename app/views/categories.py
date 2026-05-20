from collections import Counter

from nicegui import ui

from app.data_access.db import engine, get_session
from app.data_access.dao import CategoryDAO, ProductDAO, StorageLocationDAO
from app.services.category_services import CategoryServices
from app.services.product_services import ProductServices

from .layout import render_shell


def _get_category_service() -> CategoryServices:
    category_dao = CategoryDAO(engine)
    product_dao = ProductDAO(engine)

    return CategoryServices(
        category_dao,
        product_dao,
    )


def _build_rows() -> list[dict]:
    category_dao = CategoryDAO(engine)
    product_dao = ProductDAO(engine)

    category_service = CategoryServices(
        category_dao,
        product_dao,
    )

    product_service = ProductServices(
        product_dao,
        category_dao,
        StorageLocationDAO(engine),
    )

    with get_session() as session:
        categories = category_service.get_all_categories(session)
        products = product_service.get_all_products(session)

    product_count = Counter(
        product.category_id for product in products
    )

    rows: list[dict] = []

    for category in categories:
        rows.append(
            {
                "category_id": category.category_id,
                "name": category.name,
                "type": category.type,
                "products": product_count.get(
                    category.category_id,
                    0,
                ),
            }
        )

    return rows


@ui.page("/categories")
def categories_page() -> None:

    def content() -> None:

        rows = _build_rows()

        category_service = _get_category_service()

        with ui.card().classes(
            "rounded-3xl p-6 shadow-sm w-full"
        ):

            with ui.row().classes(
                "w-full items-center justify-between"
            ):

                with ui.column():
                    ui.label(
                        "Categories"
                    ).classes(
                        "text-xl font-semibold text-gray-900"
                    )

                    ui.label(
                        "Manage product groups and category types."
                    ).classes(
                        "text-sm text-gray-500"
                    )

                add_dialog = ui.dialog()

                with add_dialog, ui.card().classes(
                    "rounded-2xl p-6 w-96"
                ):

                    ui.label(
                        "Add Category"
                    ).classes(
                        "text-lg font-semibold"
                    )

                    name_input = ui.input(
                        "Category name"
                    ).classes(
                        "w-full"
                    )

                    type_input = ui.select(
                        ["sale", "loan"],
                        label="Category type",
                        value="sale",
                    ).classes(
                        "w-full"
                    )

                    message = ui.label("").classes(
                        "text-red-500 text-sm"
                    )

                    def save_category() -> None:

                        name = str(
                            name_input.value or ""
                        ).strip()

                        category_type = str(
                            type_input.value or "sale"
                        ).strip()

                        if not name:
                            message.set_text(
                                "Category name is required."
                            )
                            return

                        try:
                            with get_session() as session:

                                category_service.create_category(
                                    session,
                                    {
                                        "name": name,
                                        "type": category_type,
                                    },
                                )

                            ui.notify(
                                "Category created successfully.",
                                color="green",
                            )

                            add_dialog.close()

                            ui.navigate.reload()

                        except ValueError as error:

                            message.set_text(
                                str(error)
                            )

                    with ui.row().classes(
                        "w-full justify-end gap-2 mt-4"
                    ):

                        ui.button(
                            "Cancel",
                            on_click=add_dialog.close,
                        ).props("flat")

                        ui.button(
                            "Save",
                            on_click=save_category,
                        ).classes(
                            "bg-blue-600 text-white"
                        )

                ui.button(
                    "+ Add Category",
                    on_click=add_dialog.open,
                ).classes(
                    "bg-blue-600 text-white"
                )

            ui.separator().classes("my-4")

            if not rows:

                ui.label(
                    "No categories found."
                ).classes(
                    "text-base text-gray-500"
                )

                return

            table = ui.table(
                columns=[
                    {
                        "name": "category_id",
                        "label": "ID",
                        "field": "category_id",
                    },
                    {
                        "name": "name",
                        "label": "Name",
                        "field": "name",
                    },
                    {
                        "name": "type",
                        "label": "Type",
                        "field": "type",
                    },
                    {
                        "name": "products",
                        "label": "Products",
                        "field": "products",
                    },
                    {
                        "name": "actions",
                        "label": "Actions",
                        "field": "actions",
                    },
                ],
                rows=rows,
                row_key="category_id",
            ).classes("w-full")

            def delete_category(
                category_id: int
            ) -> None:

                try:
                    with get_session() as session:

                        category_service.delete_category(
                            session,
                            category_id,
                        )

                    ui.notify(
                        "Category deleted successfully.",
                        color="green",
                    )

                    ui.navigate.reload()

                except ValueError as error:

                    ui.notify(
                        str(error),
                        color="red",
                    )

            table.add_slot(
                "body-cell-actions",
                """
                <q-td :props="props">
                    <q-btn
                        flat
                        round
                        dense
                        color="red"
                        icon="delete"
                        @click="$parent.$emit(
                            'delete_category',
                            props.row.category_id
                        )"
                    />
                </q-td>
                """
            )

            table.on(
                "delete_category",
                lambda event: delete_category(
                    event.args
                ),
            )

    render_shell(
        "Categories",
        "Organize products by category and track usage.",
        "/categories",
        content,
    )

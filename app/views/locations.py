from nicegui import ui

from app.models import StorageLocation
from app.views.auth_state import current_user

from app.data_access.db import engine, get_session
from app.data_access.dao import (
    CategoryDAO,
    ProductDAO,
    StorageLocationDAO,
)

from app.services.location_services import LocationServices
from app.services.product_services import ProductServices

from .layout import render_shell


location_service = LocationServices(StorageLocationDAO(engine))


def _get_user_role():
    return current_user.get("role")


def _load_location_data() -> dict:
    location_dao = StorageLocationDAO(engine)
    product_dao = ProductDAO(engine)

    location_service_local = LocationServices(location_dao)

    product_service = ProductServices(
        product_dao,
        CategoryDAO(engine),
        location_dao,
    )

    with get_session() as session:
        locations = location_service_local.get_all_storage_locations(session)
        products = product_service.get_all_products(session)

    product_count: dict[int, int] = {}
    stock_by_location: dict[int, int] = {}

    for product in products:
        location_id = product.storage_location_id

        product_count[location_id] = product_count.get(location_id, 0) + 1
        stock_by_location[location_id] = (
            stock_by_location.get(location_id, 0) + product.quantity
        )

    rows = []

    for location in locations:
        units = stock_by_location.get(location.storage_location_id, 0)

        products_in_location = product_count.get(
            location.storage_location_id,
            0,
        )

        rows.append({
            "id": location.storage_location_id,
            "name": location.name,
            "shelf": location.shelf_number or "-",
            "products": products_in_location,
            "units": units,
            "status": "Active" if products_in_location > 0 else "Empty",
            "utilization": min(units * 5, 100),
        })

    chart_labels = [row["name"] for row in rows]
    chart_values = [row["units"] for row in rows]

    active_count = len([
        row for row in rows
        if row["status"] == "Active"
    ])

    empty_count = len([
        row for row in rows
        if row["status"] == "Empty"
    ])

    total_units = sum(row["units"] for row in rows)

    return {
        "total_locations": len(rows),
        "active_locations": active_count,
        "empty_locations": empty_count,
        "stored_products": len(products),
        "total_units": total_units,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "rows": rows,
    }


def _add_location_dialog():
    with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
        ui.label("Add New Location").classes("text-xl font-semibold")

        name_input = ui.input("Location name").classes("w-full")
        shelf_input = ui.input("Shelf number").classes("w-full")

        def create_location():
            name = str(name_input.value or "").strip()
            shelf_number = str(shelf_input.value or "").strip()

            if not name:
                ui.notify("Please enter a location name.", color="orange")
                return

            new_location = StorageLocation(
                name=name,
                shelf_number=shelf_number or None,
            )

            with get_session() as session:
                try:
                    location_dao = StorageLocationDAO(engine)

                    location_dao.create(
                        session,
                        new_location,
                    )

                    ui.notify(
                        "Location created successfully",
                        color="green",
                    )

                    dialog.close()
                    ui.navigate.to("/locations")

                except Exception as e:
                    ui.notify(str(e), color="red")

        with ui.row().classes("justify-end w-full mt-4"):
            ui.button(
                "Cancel",
                on_click=dialog.close,
            ).props("flat")

            ui.button(
                "Create",
                on_click=create_location,
            ).props("color=primary")

    dialog.open()


def _edit_location_dialog(location_id: int):
    location_dao = StorageLocationDAO(engine)

    with get_session() as session:
        location = location_dao.get(session, location_id)

        if not location:
            ui.notify("Location not found.", color="red")
            return

        current_name = location.name
        current_shelf = location.shelf_number or ""

    with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
        ui.label("Edit Location").classes("text-xl font-semibold")

        name_input = ui.input(
            "Location name",
            value=current_name,
        ).classes("w-full")

        shelf_input = ui.input(
            "Shelf number",
            value=current_shelf,
        ).classes("w-full")

        def save_location():
            name = str(name_input.value or "").strip()
            shelf_number = str(shelf_input.value or "").strip()

            if not name:
                ui.notify("Please enter a location name.", color="orange")
                return

            with get_session() as session:
                try:
                    location_dao = StorageLocationDAO(engine)

                    location_dao.update(
                        session,
                        location_id,
                        {
                            "name": name,
                            "shelf_number": shelf_number or None,
                        },
                    )

                    ui.notify(
                        "Location updated successfully",
                        color="green",
                    )

                    dialog.close()
                    ui.navigate.to("/locations")

                except Exception as e:
                    ui.notify(str(e), color="red")

        with ui.row().classes("justify-end w-full mt-4"):
            ui.button(
                "Cancel",
                on_click=dialog.close,
            ).props("flat")

            ui.button(
                "Save",
                on_click=save_location,
            ).props("color=primary")

    dialog.open()


def _confirm_delete_location(location_id: int):
    with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
        ui.label("Delete Location").classes(
            "text-xl font-semibold text-red-600"
        )

        ui.label(
            "Are you sure you want to delete this location?"
        ).classes(
            "text-sm text-gray-600 mt-2"
        )

        ui.label(
            "Locations with assigned products cannot be deleted."
        ).classes(
            "text-xs text-gray-500 mt-1"
        )

        with ui.row().classes("justify-end w-full mt-4"):
            ui.button(
                "Cancel",
                on_click=dialog.close,
            ).props("flat")

            ui.button(
                "Delete",
                on_click=lambda: (
                    dialog.close(),
                    _delete_location(location_id),
                ),
            ).props("color=negative")

    dialog.open()


def _delete_location(location_id: int):
    location_dao = StorageLocationDAO(engine)
    product_dao = ProductDAO(engine)

    with get_session() as session:
        try:
            products = product_dao.get_all(session)

            assigned_products = [
                product for product in products
                if product.storage_location_id == location_id
            ]

            if assigned_products:
                ui.notify(
                    "Cannot delete location because products are still assigned to it.",
                    color="orange",
                )
                return

            location_dao.delete(session, location_id)

            ui.notify(
                "Location deleted successfully",
                color="green",
            )

            ui.navigate.to("/locations")

        except Exception as e:
            ui.notify(str(e), color="red")


def _stat_card(
    title: str,
    value: str,
    icon: str,
    icon_color: str,
):
    with ui.card().classes(
        "flex-1 min-w-[180px] rounded-2xl p-4 shadow-sm"
    ):
        with ui.row().classes("items-center gap-3"):
            ui.icon(icon).classes(f"text-2xl {icon_color}")

            with ui.column().classes("gap-0"):
                ui.label(value).classes(
                    "text-2xl font-bold text-gray-900"
                )

                ui.label(title).classes(
                    "text-sm text-gray-500"
                )


@ui.page("/locations")
def locations_page() -> None:
    def content() -> None:
        data = _load_location_data()
        is_admin = _get_user_role() == "admin"

        ui.add_css("""
        .q-table tbody tr:hover {
            background-color: #f5f8ff;
            transition: 0.2s;
        }
        """)

        with ui.row().classes("w-full gap-4 flex-wrap"):
            _stat_card(
                "Total Locations",
                str(data["total_locations"]),
                "place",
                "text-blue-500",
            )

            _stat_card(
                "Active Locations",
                str(data["active_locations"]),
                "check_circle",
                "text-green-500",
            )

            _stat_card(
                "Empty Locations",
                str(data["empty_locations"]),
                "inventory_2",
                "text-orange-500",
            )

            _stat_card(
                "Stored Products",
                str(data["stored_products"]),
                "category",
                "text-indigo-500",
            )

            _stat_card(
                "Total Units",
                str(data["total_units"]),
                "monitoring",
                "text-blue-500",
            )

        with ui.row().classes(
            "w-full gap-6 flex-wrap items-start mt-6"
        ):
            with ui.card().classes(
                "flex-1 min-w-[420px] rounded-3xl p-6 shadow-sm"
            ):
                ui.label("Location Overview").classes(
                    "text-xl font-semibold text-gray-900"
                )

                ui.label(
                    "Stock distribution by storage location"
                ).classes(
                    "text-sm text-gray-500 mb-4"
                )

                if not data["chart_values"]:
                    ui.label("No location data available.").classes(
                        "text-gray-500"
                    )
                else:
                    ui.echart({
                        "tooltip": {
                            "trigger": "axis"
                        },
                        "xAxis": {
                            "type": "category",
                            "data": data["chart_labels"],
                        },
                        "yAxis": {
                            "type": "value"
                        },
                        "series": [
                            {
                                "name": "Units",
                                "type": "bar",
                                "data": data["chart_values"],
                                "itemStyle": {
                                    "color": "#4f73df"
                                },
                            }
                        ],
                    }).classes("w-full h-96")

            with ui.card().classes(
                "flex-[2] min-w-[520px] rounded-3xl p-6 shadow-sm"
            ):
                with ui.row().classes(
                    "w-full items-center justify-between"
                ):
                    with ui.column().classes("gap-0"):
                        ui.label("All Locations").classes(
                            "text-xl font-semibold text-gray-900"
                        )

                        ui.label(
                            "Overview of shelves and stored products"
                        ).classes(
                            "text-sm text-gray-500"
                        )

                    if is_admin:
                        ui.button(
                            "+ Add Location",
                            on_click=_add_location_dialog,
                        ).props(
                            "unelevated"
                        ).classes(
                            "bg-blue-500 text-white rounded-xl px-4 py-2"
                        )

                ui.separator().classes("my-4")

                search = ui.input(
                    "Search locations",
                    placeholder="Search by name, shelf or status...",
                ).props(
                    "outlined dense clearable"
                ).classes("w-full mb-4")

                columns = [
                    {
                        "name": "id",
                        "label": "ID",
                        "field": "id",
                    },
                    {
                        "name": "name",
                        "label": "Location Name",
                        "field": "name",
                    },
                    {
                        "name": "shelf",
                        "label": "Shelf",
                        "field": "shelf",
                    },
                    {
                        "name": "products",
                        "label": "Products",
                        "field": "products",
                    },
                    {
                        "name": "units",
                        "label": "Units",
                        "field": "units",
                    },
                    {
                        "name": "status",
                        "label": "Status",
                        "field": "status",
                    },
                    {
                        "name": "utilization",
                        "label": "Utilization",
                        "field": "utilization",
                    },
                ]

                if is_admin:
                    columns.append({
                        "name": "actions",
                        "label": "Actions",
                        "field": "actions",
                    })

                table = ui.table(
                    columns=columns,
                    rows=data["rows"],
                    row_key="id",
                ).classes("w-full")

                table.props("flat bordered separator=horizontal")
                search.bind_value(table, "filter")

                table.add_slot(
                    "body-cell-status",
                    """
                    <q-td :props="props">
                        <q-badge
                            :color="props.row.status === 'Active'
                                ? 'positive'
                                : 'orange'"
                            text-color="white"
                            rounded
                        >
                            {{ props.row.status }}
                        </q-badge>
                    </q-td>
                    """,
                )

                table.add_slot(
                    "body-cell-utilization",
                    """
                    <q-td :props="props">
                        <div class="row items-center no-wrap" style="gap: 10px;">
                            <span style="min-width: 38px;">
                                {{ props.row.utilization }}%
                            </span>

                            <q-linear-progress
                                size="10px"
                                :value="props.row.utilization / 100"
                                color="blue"
                                rounded
                                style="width: 90px;"
                            />
                        </div>
                    </q-td>
                    """,
                )

                if is_admin:
                    table.add_slot(
                        "body-cell-actions",
                        """
                        <q-td :props="props">
                            <q-btn
                                dense
                                flat
                                icon="edit"
                                color="primary"
                                title="Edit location"
                                @click="$parent.$emit('edit-location', props.row.id)"
                            />

                            <q-btn
                                dense
                                flat
                                icon="delete"
                                color="negative"
                                title="Delete location"
                                @click="$parent.$emit('delete-location', props.row.id)"
                            />
                        </q-td>
                        """,
                    )

                    table.on(
                        "edit-location",
                        lambda e: _edit_location_dialog(e.args),
                    )

                    table.on(
                        "delete-location",
                        lambda e: _confirm_delete_location(e.args),
                    )

        with ui.card().classes(
            "rounded-3xl p-6 shadow-sm mt-6 w-full"
        ):
            ui.label("Location Summary").classes(
                "text-2xl font-semibold text-gray-900"
            )

            ui.label(
                "Overview of storage utilization and access permissions."
            ).classes(
                "text-sm text-gray-500 mt-1 mb-5"
            )

            with ui.row().classes("w-full gap-8 flex-wrap"):
                with ui.column().classes("gap-1"):
                    ui.label("Storage Usage").classes(
                        "text-lg font-semibold text-blue-600"
                    )

                    ui.label(
                        f"Active locations: {data['active_locations']}"
                    ).classes("text-gray-700")

                    ui.label(
                        f"Empty locations: {data['empty_locations']}"
                    ).classes("text-gray-700")

                    ui.label(
                        f"Total stored units: {data['total_units']}"
                    ).classes("text-gray-700")

                with ui.column().classes("gap-1"):
                    ui.label("Permissions").classes(
                        "text-lg font-semibold text-green-600"
                    )

                    ui.label(
                        "Admins can add, edit and delete locations."
                    ).classes("text-gray-700")

                    ui.label(
                        "Staff users can only view location data."
                    ).classes("text-gray-700")

                    ui.label(
                        "Locations with assigned products cannot be deleted."
                    ).classes("text-gray-700")

    render_shell(
        "Locations",
        "Manage storage areas and shelf assignments.",
        "/locations",
        content,
    )

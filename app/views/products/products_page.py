from nicegui import ui
import json

from app.data_access.db import engine, get_session
from app.data_access.dao import ProductDAO, CategoryDAO, StorageLocationDAO
from app.services.product_services import ProductServices
from app.services.category_services import CategoryServices
from app.services.location_services import LocationServices

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
                        "category_id": product.category_id,
                        "storage_location": location.name if location else "-",
                        "storage_location_id": product.storage_location_id,
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

        # Fetch categories and locations for select options using services
        category_dao = CategoryDAO(engine)
        location_dao = StorageLocationDAO(engine)
        category_service = CategoryServices(category_dao, ProductDAO(engine))
        location_service = LocationServices(location_dao)
        categories = []
        locations = []
        cat_by_id = {}
        loc_by_id = {}
        with get_session() as session:
            categories = category_service.get_all_categories(session)
            locations = location_service.get_all_storage_locations(session)
            cat_by_id = {c.category_id: c.name for c in categories}
            loc_by_id = {l.storage_location_id: l.name for l in locations}

        # editable fields for quick actions
        editable_fields = ["name", "quantity", "minimum_stock", "status"]

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

        def add_product() -> None:
            try:
                category_dao = CategoryDAO(engine)
                location_dao = StorageLocationDAO(engine)
                product_dao = ProductDAO(engine)
                product_service = ProductServices(product_dao, category_dao, location_dao)

                categories = []
                locations = []
                with get_session() as session:
                    categories = category_dao.get_all(session)
                    locations = location_dao.get_all(session)

                if not categories or not locations:
                    ui.notify("Please add categories and locations first", type="warning")
                    return

                options_cat = {c.category_id: c.name for c in categories}
                options_loc = {l.storage_location_id: l.name for l in locations}

                with ui.dialog() as dialog, ui.card().classes("w-96"):
                    ui.label("Add product").classes("text-lg font-semibold")

                    name = ui.input("Name").classes("w-full")

                    category = ui.select(
                        options=options_cat,
                        label="Category",
                        value=next(iter(options_cat)),
                    ).classes("w-full")

                    location = ui.select(
                        options=options_loc,
                        label="Storage Location",
                        value=next(iter(options_loc)),
                    ).classes("w-full")

                    quantity = ui.number("Quantity", value=0).classes("w-full")
                    minimum_stock = ui.number("Min stock", value=0).classes("w-full")
                    status = ui.input("Status", value="active").classes("w-full")

                    def save_new() -> None:
                        data = {
                            "name": name.value,
                            "category_id": category.value,
                            "storage_location_id": location.value,
                            "quantity": int(quantity.value),
                            "minimum_stock": int(minimum_stock.value),
                            "status": status.value,
                        }
                        try:
                            with get_session() as session:
                                product_service.create_product(session, data)

                            ui.notify("Product created", type="positive")
                            dialog.close()
                            ui.navigate.reload()
                        except ValueError as error:
                            ui.notify(str(error), type="negative")

                    with ui.row().classes("justify-end w-full"):
                        ui.button("Cancel", on_click=dialog.close)
                        ui.button("Create", color="primary", on_click=save_new)

                dialog.open()
            except Exception as e:
                ui.notify(f"Error: {str(e)}", type="negative")

        def handle_save(event_args) -> None:
            payload = event_args
            if isinstance(payload, list):
                payload = payload[0]
            if not isinstance(payload, dict):
                return
            row = payload.get("row")
            field = payload.get("field")
            if not row or not field:
                return
            product_dao = ProductDAO(engine)
            category_dao_inst = CategoryDAO(engine)
            location_dao_inst = StorageLocationDAO(engine)
            product_service = ProductServices(product_dao, category_dao_inst, location_dao_inst)
            
            # Map field names for special cases
            data = {}
            if field == "category":
                data["category_id"] = int(row.get("category_id", 0))
            elif field == "storage_location":
                data["storage_location_id"] = int(row.get("storage_location_id", 0))
            else:
                data[field] = row[field]
            
            try:
                with get_session() as session:
                    product_service.update_product(session, row["product_id"], data)
                ui.notify("Product updated", type="positive")
                ui.navigate.reload()
            except ValueError as error:
                ui.notify(str(error), type="negative")

        with ui.card().classes("w-full rounded-3xl p-6 shadow-sm"):
            with ui.column().classes("w-full items-center justify-between"):
                ui.label("Products").classes("text-xl font-semibold text-gray-900")
                ui.label("Browse and manage your inventory items.").classes("text-gray-500"
                )
                with ui.row().classes("w-full justify-end"):
                    ui.button("Add Product", color="primary", on_click=add_product)
                
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

            # add inline editable slots for key fields
            table.add_slot(
                "body-cell-name",
                """
<q-td :props="props">
  <div v-if="!props.row._editing_field || props.row._editing_field!='name'"
       @click="props.row._editing_row ? props.row._editing_field='name' : null"
       @dblclick="props.row._editing_field='name'">
       {{ props.value }}
  </div>
  <div v-else>
    <q-input dense v-model="props.row.name"
             @blur="$parent.$emit('save', {row: props.row, field: 'name'})"
             @keyup.enter="$parent.$emit('save', {row: props.row, field: 'name'})" />
  </div>
</q-td>
""",
            )

            table.add_slot(
                "body-cell-quantity",
                """
<q-td :props="props">
  <div v-if="!props.row._editing_field || props.row._editing_field!='quantity'"
       @click="props.row._editing_row ? props.row._editing_field='quantity' : null"
       @dblclick="props.row._editing_field='quantity'">
       {{ props.value }}
  </div>
  <div v-else>
    <q-input dense type="number" v-model="props.row.quantity"
             @blur="$parent.$emit('save', {row: props.row, field: 'quantity'})"
             @keyup.enter="$parent.$emit('save', {row: props.row, field: 'quantity'})" />
  </div>
</q-td>
""",
            )

            table.add_slot(
                "body-cell-minimum_stock",
                """
<q-td :props="props">
  <div v-if="!props.row._editing_field || props.row._editing_field!='minimum_stock'"
       @click="props.row._editing_row ? props.row._editing_field='minimum_stock' : null"
       @dblclick="props.row._editing_field='minimum_stock'">
       {{ props.value }}
  </div>
  <div v-else>
    <q-input dense type="number" v-model="props.row.minimum_stock"
             @blur="$parent.$emit('save', {row: props.row, field: 'minimum_stock'})"
             @keyup.enter="$parent.$emit('save', {row: props.row, field: 'minimum_stock'})" />
  </div>
</q-td>
""",
            )

            table.add_slot(
                "body-cell-status",
                """
<q-td :props="props">
  <div v-if="!props.row._editing_field || props.row._editing_field!='status'"
       @click="props.row._editing_row ? props.row._editing_field='status' : null"
       @dblclick="props.row._editing_field='status'">
       {{ props.value }}
  </div>
  <div v-else>
    <q-input dense v-model="props.row.status"
             @blur="$parent.$emit('save', {row: props.row, field: 'status'})"
             @keyup.enter="$parent.$emit('save', {row: props.row, field: 'status'})" />
  </div>
</q-td>
""",
            )
            
            cat_options_list = [{"label": c.name, "value": c.category_id} for c in categories]
            cat_options_json = json.dumps(cat_options_list)

            table.add_slot(
    "body-cell-category",
    f"""
<q-td :props="props">
  <div v-if="props.row._editing_field !== 'category'"
       @click="props.row._editing_row ? props.row._editing_field = 'category' : null"
       @dblclick="props.row._editing_field = 'category'">
    {{{{ props.value }}}}
  </div>

  <q-select v-else
            dense
            emit-value
            map-options
            v-model="props.row.category_id"
            :options='{cat_options_json}'
            @update:model-value="$parent.$emit('save', {{row: props.row, field: 'category'}})" />
</q-td>
""",
            )
            loc_options_list = [{"label": l.name, "value": l.storage_location_id} for l in locations]
            loc_options_json = json.dumps(loc_options_list)

            table.add_slot(
    "body-cell-storage_location",
    f"""
<q-td :props="props">
    <div v-if="props.row._editing_field !== 'storage_location'"
            @click="props.row._editing_row ? props.row._editing_field = 'storage_location' : null"
            @dblclick="props.row._editing_field = 'storage_location'">
        {{{{ props.value }}}}
    </div>
    <q-select v-else
            dense
            emit-value
            map-options
            v-model="props.row.storage_location_id"
            :options='{loc_options_json}'
            @update:model-value="$parent.$emit('save', {{row: props.row, field: 'storage_location'}})" />
</q-td>
""",
            )
            loc_options_list = [{"label": l.name, "value": l.storage_location_id} for l in locations]
            loc_options_json = json.dumps(loc_options_list)

            table.add_slot(
    "body-cell-storage_location",
    f"""
<q-td :props="props">
    <div v-if="props.row._editing_field !== 'storage_location'"
            @click="props.row._editing_row ? props.row._editing_field = 'storage_location' : null"
            
            @dblclick="props.row._editing_field = 'storage_location'">
        {{{{ props.value }}}}
    </div>
    <q-select v-else
            dense
            emit-value
            map-options
            v-model="props.row.storage_location_id"
            :options='{loc_options_json}'
            @update:model-value="$parent.$emit('save', {{row: props.row, field: 'storage_location'}})" />
</q-td>
""",
            )
            
            cat_options_list = [{"label": c.name, "value": c.category_id} for c in categories]
            cat_options_json = json.dumps(cat_options_list)

            table.add_slot(
                "body-cell-actions",
                """
<q-td :props="props">
    <q-btn dense flat color="primary" icon="edit" label="Bearbeiten"
           @click="props.row._editing_row=true" />
    <q-btn dense flat color="negative" icon="delete" label="Löschen"
           @click="$parent.$emit('delete', props.row)" />
</q-td>
""",
            )

            table.on("delete", lambda e: delete_row(e.args))
            table.on("save", lambda e: handle_save(e.args))

    render_shell("Products", "Inventory items and their details.", "/products", content)

from nicegui import ui
import json

from app.data_access.db import engine, get_session
from app.data_access.dao import ProductDAO, CategoryDAO, StorageLocationDAO
from app.services.product_services import ProductServices
from app.services.category_services import CategoryServices
from app.services.location_services import LocationServices

from .layout import render_shell


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
        all_rows = _build_rows()

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
                    ui.label("Add Product").classes("text-lg font-semibold")

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

        total_products = len(all_rows)
        low_stock = sum(1 for row in all_rows if int(row["quantity"]) <= int(row["minimum_stock"]))
        category_count = len({row["category_id"] for row in all_rows})
        total_units = sum(int(row["quantity"]) for row in all_rows)

        status_values = sorted({str(row.get("status", "")).strip() for row in all_rows if row.get("status")})

        search_value = {"value": ""}
        category_filter_value = {"value": "all"}
        status_filter_value = {"value": "all"}

        table = None
        table_count_label = None

        def get_filtered_rows() -> list[dict]:
            text = search_value["value"].strip().lower()
            selected_category = category_filter_value["value"]
            selected_status = status_filter_value["value"]

            filtered: list[dict] = []
            for row in all_rows:
                if selected_category != "all" and str(row.get("category_id")) != str(selected_category):
                    continue
                if selected_status != "all" and str(row.get("status", "")).lower() != str(selected_status).lower():
                    continue

                if text:
                    haystack = " ".join(
                        [
                            str(row.get("name", "")),
                            str(row.get("category", "")),
                            str(row.get("storage_location", "")),
                            str(row.get("status", "")),
                            str(row.get("product_id", "")),
                        ]
                    ).lower()
                    if text not in haystack:
                        continue

                filtered.append(row)
            return filtered

        def refresh_table() -> None:
            filtered = get_filtered_rows()
            if table is not None:
                table.rows = filtered
                table.update()
            if table_count_label is not None:
                table_count_label.set_text(f"Showing {len(filtered)} of {len(all_rows)} products")

        with ui.column().classes("w-full gap-5"):
            with ui.card().classes("w-full rounded-3xl p-6 shadow-sm border border-gray-100"):
                with ui.row().classes("w-full items-center justify-between"):
                    with ui.row().classes("items-center gap-4"):
                        with ui.card().classes("w-14 h-14 rounded-2xl shadow-none bg-blue-50 flex items-center justify-center"):
                            ui.icon("inventory_2").classes("text-blue-600 text-3xl")
                        with ui.column().classes("gap-0"):
                            ui.label("Products").classes("text-3xl font-bold text-slate-900")
                            ui.label("Manage and view all inventory products.").classes("text-sm text-slate-500")
                    ui.button("Add Product", icon="add", color="primary", on_click=add_product).props("unelevated").classes("rounded-xl px-4")

            with ui.row().classes("w-full gap-4 no-wrap"):
                stat_cards = [
                    ("inventory_2", "Total Products", str(total_products), "bg-blue-50 text-blue-600"),
                    ("warning_amber", "Low Stock", str(low_stock), "bg-amber-50 text-amber-600"),
                    ("category", "Categories", str(category_count), "bg-emerald-50 text-emerald-600"),
                    ("widgets", "Total Units", str(total_units), "bg-purple-50 text-purple-600"),
                ]
                for icon_name, label_text, value_text, icon_style in stat_cards:
                    with ui.card().classes("w-full rounded-2xl p-4 shadow-sm border border-gray-100"):
                        with ui.row().classes("w-full items-center justify-between"):
                            with ui.row().classes("items-center gap-3"):
                                with ui.card().classes(f"w-10 h-10 rounded-xl shadow-none {icon_style} flex items-center justify-center"):
                                    ui.icon(icon_name)
                                with ui.column().classes("gap-0"):
                                    ui.label(value_text).classes("text-2xl font-bold text-slate-900")
                                    ui.label(label_text).classes("text-xs text-slate-500")
                            ui.icon("north_east").classes("text-slate-400 text-sm")

            with ui.card().classes("w-full rounded-2xl p-4 shadow-sm border border-gray-100"):
                with ui.row().classes("w-full items-center gap-3"):
                    search_input = ui.input(placeholder="Search products...").props("outlined dense clearable")
                    search_input.classes("w-[40%]")

                    category_options = {"all": "All Categories", **{str(c.category_id): c.name for c in categories}}
                    category_select = ui.select(
                        options=category_options,
                        value="all",
                    ).props("outlined dense")
                    category_select.classes("w-[25%]")

                    status_options = {"all": "All Statuses", **{s: s.capitalize() for s in status_values}}
                    status_select = ui.select(
                        options=status_options,
                        value="all",
                    ).props("outlined dense")
                    status_select.classes("w-[25%]")

                    def reset_filters() -> None:
                        search_input.value = ""
                        category_select.value = "all"
                        status_select.value = "all"
                        search_value["value"] = ""
                        category_filter_value["value"] = "all"
                        status_filter_value["value"] = "all"
                        refresh_table()

                    ui.button("Reset", icon="refresh", on_click=reset_filters).props("flat")

                    search_input.on_value_change(lambda e: (search_value.__setitem__("value", e.value or ""), refresh_table()))
                    category_select.on_value_change(lambda e: (category_filter_value.__setitem__("value", e.value or "all"), refresh_table()))
                    status_select.on_value_change(lambda e: (status_filter_value.__setitem__("value", e.value or "all"), refresh_table()))

            with ui.card().classes("w-full rounded-2xl p-0 shadow-sm border border-gray-100 overflow-hidden"):
                filtered_rows = get_filtered_rows()
                table = ui.table(
                    columns=[
                        {"name": "product_id", "label": "ID", "field": "product_id", "sortable": True},
                        {"name": "name", "label": "Product Name", "field": "name", "sortable": True},
                        {"name": "category", "label": "Category", "field": "category", "sortable": True},
                        {"name": "storage_location", "label": "Location", "field": "storage_location", "sortable": True},
                        {"name": "quantity", "label": "Quantity", "field": "quantity", "sortable": True},
                        {"name": "minimum_stock", "label": "Min. Stock", "field": "minimum_stock", "sortable": True},
                        {"name": "status", "label": "Status", "field": "status", "sortable": True},
                        {"name": "actions", "label": "Actions", "field": "actions"},
                    ],
                    rows=filtered_rows,
                    row_key="product_id",
                    pagination={"rowsPerPage": 8, "sortBy": "product_id", "descending": False},
                ).props(
                    'flat bordered separator="horizontal" row-class="(row) => row._editing_row ? \'bg-blue-1\' : \'\'"'
                ).classes("w-full")

                table.add_slot(
                    "body-cell-name",
                    """
<q-td :props="props" :class="props.row._editing_row ? 'bg-blue-1' : ''">
  <div v-if="!props.row._editing_field || props.row._editing_field !== 'name'"
       @click="props.row._editing_row ? props.row._editing_field = 'name' : null">
       {{ props.value || '(Unnamed Product)' }}
  </div>
  <q-input v-else dense v-model="props.row.name"
           @blur="$parent.$emit('save', {row: props.row, field: 'name'})"
           @keyup.enter="$parent.$emit('save', {row: props.row, field: 'name'})" />
</q-td>
""",
                )

                table.add_slot(
                    "body-cell-quantity",
                    """
<q-td :props="props" :class="props.row._editing_row ? 'bg-blue-1' : ''">
  <div v-if="!props.row._editing_field || props.row._editing_field !== 'quantity'"
       @click="props.row._editing_row ? props.row._editing_field = 'quantity' : null">
       {{ props.value }}
  </div>
  <q-input v-else dense type="number" v-model="props.row.quantity"
           @blur="$parent.$emit('save', {row: props.row, field: 'quantity'})"
           @keyup.enter="$parent.$emit('save', {row: props.row, field: 'quantity'})" />
</q-td>
""",
                )

                table.add_slot(
                    "body-cell-minimum_stock",
                    """
<q-td :props="props" :class="props.row._editing_row ? 'bg-blue-1' : ''">
  <div v-if="!props.row._editing_field || props.row._editing_field !== 'minimum_stock'"
       @click="props.row._editing_row ? props.row._editing_field = 'minimum_stock' : null">
       {{ props.value }}
  </div>
  <q-input v-else dense type="number" v-model="props.row.minimum_stock"
           @blur="$parent.$emit('save', {row: props.row, field: 'minimum_stock'})"
           @keyup.enter="$parent.$emit('save', {row: props.row, field: 'minimum_stock'})" />
</q-td>
""",
                )

                cat_options_list = [{"label": c.name, "value": c.category_id} for c in categories]
                cat_options_json = json.dumps(cat_options_list)
                table.add_slot(
                    "body-cell-category",
                    f"""
<q-td :props="props" :class="props.row._editing_row ? 'bg-blue-1' : ''">
  <div v-if="props.row._editing_field !== 'category'"
       @click="props.row._editing_row ? props.row._editing_field = 'category' : null">
    <q-badge rounded color="blue-1" text-color="primary">{{{{ props.value }}}}</q-badge>
  </div>
  <q-select v-else dense emit-value map-options v-model="props.row.category_id"
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
<q-td :props="props" :class="props.row._editing_row ? 'bg-blue-1' : ''">
  <div v-if="props.row._editing_field !== 'storage_location'"
       @click="props.row._editing_row ? props.row._editing_field = 'storage_location' : null">
    {{{{ props.value }}}}
  </div>
  <q-select v-else dense emit-value map-options v-model="props.row.storage_location_id"
            :options='{loc_options_json}'
            @update:model-value="$parent.$emit('save', {{row: props.row, field: 'storage_location'}})" />
</q-td>
""",
                )

                table.add_slot(
                    "body-cell-status",
                    """
<q-td :props="props" :class="props.row._editing_row ? 'bg-blue-1' : ''">
  <div v-if="!props.row._editing_field || props.row._editing_field !== 'status'"
       @click="props.row._editing_row ? props.row._editing_field = 'status' : null">
    <q-badge rounded
             :color="String(props.row.status || '').toLowerCase() === 'active' ? 'green-1' : 'grey-3'"
             :text-color="String(props.row.status || '').toLowerCase() === 'active' ? 'positive' : 'dark'">
      {{ props.value }}
    </q-badge>
  </div>
  <q-input v-else dense v-model="props.row.status"
           @blur="$parent.$emit('save', {row: props.row, field: 'status'})"
           @keyup.enter="$parent.$emit('save', {row: props.row, field: 'status'})" />
</q-td>
""",
                )

                table.add_slot(
                    "body-cell-actions",
                    """
<q-td :props="props">
  <div class="row items-center q-gutter-xs no-wrap justify-end">
    <q-btn round dense flat :color="props.row._editing_row ? 'primary' : 'grey-7'"
           :icon="props.row._editing_row ? 'check_circle' : 'edit'"
           @click="props.row._editing_row = !props.row._editing_row; if (!props.row._editing_row) props.row._editing_field = null">
      <q-tooltip>{{ props.row._editing_row ? 'Finish Inline Edit' : 'Inline Edit' }}</q-tooltip>
    </q-btn>
    <q-btn round dense flat color="negative" icon="delete"
           @click="$parent.$emit('delete', props.row)">
      <q-tooltip>Delete Product</q-tooltip>
    </q-btn>
  </div>
</q-td>
""",
                )

                table.on("delete", lambda e: delete_row(e.args))
                table.on("save", lambda e: handle_save(e.args))

                with ui.row().classes("w-full justify-between items-center px-4 py-3 text-sm text-slate-500"):
                    table_count_label = ui.label(f"Showing {len(filtered_rows)} of {len(all_rows)} products")
                    ui.label("Tip: Click edit, then click a cell to update inline.")

            if not all_rows:
                ui.notify("No products found.", type="warning")

    render_shell("Products", "Inventory items and their details.", "/products", content)

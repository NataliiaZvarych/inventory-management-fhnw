from nicegui import ui
from app.data_access.db import get_session, engine
from app.services import *
from app.data_access.dao import (
    UserDAO,
    ProductDAO,
    CategoryDAO,
    StorageLocationDAO,
    StockMovementDAO,
)


product_services = ProductServices(
    ProductDAO(engine),
    CategoryDAO(engine),
    StorageLocationDAO(engine)
)
category_services = CategoryServices(CategoryDAO(engine), ProductDAO(engine))
location_services = LocationServices(StorageLocationDAO(engine))
movement_services = MovementService(
    ProductDAO(engine),
    UserDAO(engine),
    StockMovementDAO(engine),
    StorageLocationDAO(engine)
)
user_services = UserService(UserDAO(engine)) 
current_user = {
    "user_id": None,
    "name": None,
    "role": None,
}


@ui.page("/")
def login_page():
    with ui.column().classes("items-center justify-center h-screen w-full bg-gray-50"):
        with ui.card().classes("p-8 w-96 shadow-lg"):
            ui.label("📦 Lagerverwaltung").classes("text-3xl font-bold")
            ui.label("Inventarsystem").classes("text-gray-500 mb-4")

            user_input = ui.input("Username or User ID").classes("w-full")

            password_input = ui.input(
                "Password optional",
                password=True,
                password_toggle_button=True
            ).classes("w-full")

            message = ui.label("").classes("text-red-500")

            def login():
                value = str(user_input.value).strip()

                if not value:
                    message.set_text("Please enter username or user ID.")
                    return

                with get_session() as session:
                    try:
                        if value.isdigit():
                            user = user_services.get_user(
                                session,
                                int(value)
                            )
                        else:
                            users = user_services.user_dao.get_all(session)
                            user = next(
                                (u for u in users if u.name == value),
                                None
                            )

                            if not user:
                                raise ValueError("User not found")

                        current_user["user_id"] = user.user_id
                        current_user["name"] = user.name
                        current_user["role"] = user.role

                        ui.notify(
                            f"Welcome, {user.name}!",
                            color="green"
                        )

                        ui.navigate.to("/dashboard")

                    except ValueError as e:
                        message.set_text(str(e))

            ui.button("Login", on_click=login).classes("w-full mt-4")


def menu_button(icon: str, text: str, target: str):
    ui.button(
        f"{icon}  {text}",
        on_click=lambda: ui.navigate.to(target)
    ).props("flat").classes("w-full justify-start text-left")


@ui.page("/dashboard")
def dashboard():
    with get_session() as session:
        products = product_services.get_all_products(session)
        categories = category_services.get_all_categories(session)
        locations = location_services.get_all_storage_locations(session)
        movements = movement_services.get_all_movements(session)

    low_stock_products = [
        product for product in products
        if product.quantity <= product.minimum_stock
    ]

    latest_movements = sorted(
        movements,
        key=lambda movement: movement.timestamp,
        reverse=True
    )[:5]

    total_stock = sum(product.quantity for product in products)

    active_products = [
        product for product in products
        if getattr(product, "status", "active") == "active"
    ]

    with ui.row().classes("w-full min-h-screen bg-gray-50 no-wrap"):

        with ui.column().classes("w-56 bg-white border-r p-4 gap-3"):
            ui.label("📦 Lagerverwaltung").classes("text-xl font-bold")
            ui.label("Inventarsystem").classes("text-xs text-gray-500 mb-4")

            menu_button("📊", "Dashboard", "/dashboard")
            menu_button("📦", "Produkte", "/products")
            menu_button("🏷️", "Kategorien", "/categories")
            menu_button("📍", "Lagerorte", "/locations")
            menu_button("🔄", "Bewegungen", "/movements")

        with ui.column().classes("flex-1 p-6 gap-6"):

            with ui.row().classes("w-full justify-between items-center"):
                ui.label("Dashboard").classes("text-3xl font-bold")

                with ui.row().classes("items-center gap-4"):
                    if low_stock_products:
                        ui.badge(
                            f"⚠️ {len(low_stock_products)} Produkt(e) mit niedrigem Bestand",
                            color="warning"
                        )

                    ui.label(
                        f"🔵 {current_user['name'] or 'Unknown'}"
                    ).classes("font-semibold")

                    ui.label(
                        current_user["role"] or "-"
                    ).classes("text-sm text-gray-500")

            with ui.row().classes("gap-4"):
                with ui.card().classes("p-5 w-56 shadow-sm"):
                    ui.label("Produktarten").classes("text-sm text-gray-500")
                    ui.label(str(len(products))).classes("text-4xl font-bold")
                    ui.label("📦").classes("text-2xl")

                with ui.card().classes("p-5 w-56 shadow-sm"):
                    ui.label("Gesamtbestand").classes("text-sm text-gray-500")
                    ui.label(str(total_stock)).classes("text-4xl font-bold")
                    ui.label("📈").classes("text-2xl")

                with ui.card().classes("p-5 w-56 shadow-sm"):
                    ui.label("Niedriger Bestand").classes("text-sm text-gray-500")
                    ui.label(str(len(low_stock_products))).classes("text-4xl font-bold")
                    ui.label("⚠️").classes("text-2xl")

                with ui.card().classes("p-5 w-56 shadow-sm"):
                    ui.label("Bewegungen gesamt").classes("text-sm text-gray-500")
                    ui.label(str(len(movements))).classes("text-4xl font-bold")
                    ui.label("🔄").classes("text-2xl")

            with ui.row().classes("gap-6 w-full items-start"):

                with ui.card().classes("p-5 w-1/2 shadow-sm"):
                    ui.label("Niedriger Bestand").classes("text-xl font-bold")
                    ui.label(
                        "Produkte mit Mindestbestand erreicht oder unterschritten"
                    ).classes("text-sm text-gray-500 mb-4")

                    if not low_stock_products:
                        ui.label("Keine Produkte mit niedrigem Bestand.")
                    else:
                        for product in low_stock_products[:5]:
                            with ui.row().classes(
                                "w-full justify-between items-center bg-yellow-50 p-3 rounded-lg border"
                            ):
                                with ui.column():
                                    ui.label(product.name).classes("font-bold")
                                    ui.label(
                                        f"Minimum: {product.minimum_stock}"
                                    ).classes("text-xs text-gray-500")

                                ui.label(str(product.quantity)).classes(
                                    "text-xl font-bold text-yellow-700"
                                )

                with ui.card().classes("p-5 w-1/2 shadow-sm"):
                    ui.label("Letzte Bewegungen").classes("text-xl font-bold")
                    ui.label("Die neuesten Bestandsbewegungen").classes(
                        "text-sm text-gray-500 mb-4"
                    )

                    if not latest_movements:
                        ui.label("Keine Bewegungen gefunden.")
                    else:
                        for movement in latest_movements:
                            with ui.row().classes(
                                "w-full justify-between items-center bg-gray-50 p-3 rounded-lg border"
                            ):
                                with ui.column():
                                    ui.label(
                                        f"Product ID: {movement.product_id}"
                                    ).classes("font-bold")
                                    ui.label(str(movement.timestamp)).classes(
                                        "text-xs text-gray-500"
                                    )
                                    ui.label(movement.note or "-").classes(
                                        "text-xs text-gray-500"
                                    )

                                ui.badge(
                                    movement.movement_type,
                                    color="blue"
                                )

                                ui.label(str(movement.quantity)).classes(
                                    "text-lg font-bold"
                                )

            with ui.card().classes("p-5 w-1/2 shadow-sm"):
                ui.label("Statistiken").classes("text-xl font-bold")
                ui.label("Übersicht über das System").classes(
                    "text-sm text-gray-500 mb-4"
                )

                statistics = [
                    ("Kategorien", len(categories)),
                    ("Lagerorte", len(locations)),
                    ("Aktive Produkte", len(active_products)),
                    ("Gesamtbewegungen", len(movements)),
                ]

                for label, value in statistics:
                    with ui.row().classes(
                        "w-full justify-between bg-gray-50 p-3 rounded"
                    ):
                        ui.label(label)
                        ui.label(str(value)).classes("font-bold")
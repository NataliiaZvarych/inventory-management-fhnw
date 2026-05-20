from nicegui import ui
from app.services import UserService
from app.data_access.dao import UserDAO
from app.data_access.db import engine, get_session
from app.views.auth_state import current_user
user_services = UserService(UserDAO(engine)) 

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
            user_input.on("keydown.enter", lambda: login())
            password_input.on("keydownenter", lambda: login())
            ui.button("Login", on_click=login).classes("w-full mt-4")


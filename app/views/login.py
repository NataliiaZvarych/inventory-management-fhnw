from nicegui import ui
import hashlib

from app.services import UserService
from app.data_access.dao import UserDAO
from app.data_access.db import engine, get_session
from app.views.auth_state import current_user

user_services = UserService(UserDAO(engine))

ADMIN_RECOVERY_CODE = "FHNW-ADMIN-2026"


@ui.page("/")
def login_page():

    with ui.column().classes(
        "items-center justify-center h-screen w-full bg-gray-50"
    ):

        with ui.card().classes(
            "p-8 w-96 shadow-lg"
        ):

            ui.label("📦 Lagerverwaltung").classes(
                "text-3xl font-bold"
            )

            ui.label("Inventarsystem").classes(
                "text-gray-500 mb-4"
            )

            user_input = ui.input(
                "Username"
            ).classes("w-full")

            password_input = ui.input(
                "Password",
                password=True,
                password_toggle_button=True,
            ).classes("w-full")

            message = ui.label("").classes(
                "text-red-500"
            )

            def login():

                username = str(user_input.value or "").strip()
                password = str(password_input.value or "").strip()

                if not username:
                    message.set_text("Please enter username.")
                    return

                if not password:
                    message.set_text("Please enter password.")
                    return

                with get_session() as session:

                    try:
                        users = user_services.user_dao.get_all(session)

                        user = next(
                            (u for u in users if u.name == username),
                            None,
                        )

                        if not user:
                            raise ValueError("User not found")

                        password_hash = hashlib.sha256(
                            password.encode()
                        ).hexdigest()

                        if user.password_hash != password_hash:
                            raise ValueError("Wrong password")

                        current_user["user_id"] = user.user_id
                        current_user["name"] = user.name
                        current_user["role"] = user.role

                        ui.notify(
                            f"Welcome, {user.name}!",
                            color="green",
                        )

                        ui.navigate.to("/dashboard")

                    except ValueError as e:
                        message.set_text(str(e))

            def forgot_password_dialog():

                with ui.dialog() as dialog, ui.card().classes(
                    "p-6 w-96"
                ):

                    ui.label("Admin Password Recovery").classes(
                        "text-xl font-semibold"
                    )

                    ui.label(
                        "Only admin accounts can reset their password using the recovery code."
                    ).classes(
                        "text-sm text-gray-500 mb-3"
                    )

                    username_input = ui.input(
                        "Admin username"
                    ).classes("w-full")

                    recovery_code_input = ui.input(
                        "Recovery code",
                        password=True,
                        password_toggle_button=True,
                    ).classes("w-full")

                    new_password_input = ui.input(
                        "New password",
                        password=True,
                        password_toggle_button=True,
                    ).classes("w-full")

                    recovery_message = ui.label("").classes(
                        "text-red-500 text-sm"
                    )

                    def reset_password():

                        username = str(
                            username_input.value or ""
                        ).strip()

                        recovery_code = str(
                            recovery_code_input.value or ""
                        ).strip()

                        new_password = str(
                            new_password_input.value or ""
                        ).strip()

                        if not username:
                            recovery_message.set_text(
                                "Please enter username."
                            )
                            return

                        if not recovery_code:
                            recovery_message.set_text(
                                "Please enter recovery code."
                            )
                            return

                        if not new_password:
                            recovery_message.set_text(
                                "Please enter new password."
                            )
                            return

                        with get_session() as session:

                            try:
                                users = user_services.user_dao.get_all(
                                    session
                                )

                                user = next(
                                    (
                                        u for u in users
                                        if u.name == username
                                    ),
                                    None,
                                )

                                if not user:
                                    recovery_message.set_text(
                                        "User not found."
                                    )
                                    return

                                if user.role != "admin":
                                    recovery_message.set_text(
                                        "Only admin accounts can use recovery reset."
                                    )
                                    return

                                if recovery_code != ADMIN_RECOVERY_CODE:
                                    recovery_message.set_text(
                                        "Wrong recovery code."
                                    )
                                    return

                                password_hash = hashlib.sha256(
                                    new_password.encode()
                                ).hexdigest()

                                user_services.update_user(
                                    session,
                                    user.user_id,
                                    {
                                        "password_hash": password_hash
                                    },
                                )

                                ui.notify(
                                    "Password reset successfully.",
                                    color="green",
                                )

                                dialog.close()

                            except Exception as e:
                                recovery_message.set_text(str(e))

                    with ui.row().classes(
                        "justify-end w-full mt-4"
                    ):

                        ui.button(
                            "Cancel",
                            on_click=dialog.close,
                        ).props("flat")

                        ui.button(
                            "Reset Password",
                            on_click=reset_password,
                        ).props("color=primary")

                dialog.open()

            user_input.on(
                "keydown.enter",
                lambda: login(),
            )

            password_input.on(
                "keydown.enter",
                lambda: login(),
            )

            ui.button(
                "Login",
                on_click=login,
            ).classes("w-full mt-4")

            ui.button(
                "Forgot password?",
                on_click=forgot_password_dialog,
            ).props("flat").classes(
                "w-full mt-2 text-blue-600"
            )
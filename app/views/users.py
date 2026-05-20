from collections import Counter
import hashlib

from nicegui import ui

from app.models import User
from app.views.auth_state import current_user
from app.data_access.db import engine, get_session
from app.data_access.dao import (
    ProductDAO,
    StockMovementDAO,
    StorageLocationDAO,
    UserDAO,
)
from app.services.movement_services import MovementService
from app.services.user_service import UserService
from .layout import render_shell


user_service = UserService(UserDAO(engine))


def _get_user_role():
    return current_user.get("role")


def _load_user_data() -> dict:
    user_dao = UserDAO(engine)

    movement_service = MovementService(
        ProductDAO(engine),
        UserDAO(engine),
        StockMovementDAO(engine),
        StorageLocationDAO(engine),
    )

    with get_session() as session:
        users = user_dao.get_all(session)
        movements = movement_service.get_all_movements(session)

    movement_count = Counter(movement.user_id for movement in movements)

    rows = []
    for user in users:
        movements_total = movement_count.get(user.user_id, 0)

        rows.append({
            "user_id": user.user_id,
            "name": user.name,
            "role": user.role,
            "movements": movements_total,
            "status": "Active" if movements_total > 0 else "Inactive",
        })

    admin_count = len([row for row in rows if row["role"] == "admin"])
    staff_count = len([row for row in rows if row["role"] == "staff"])
    active_count = len([row for row in rows if row["status"] == "Active"])
    inactive_count = len([row for row in rows if row["status"] == "Inactive"])
    total_movements = sum(row["movements"] for row in rows)

    most_active_user = max(
        rows,
        key=lambda row: row["movements"],
        default=None,
    )

    return {
        "total_users": len(rows),
        "admin_count": admin_count,
        "staff_count": staff_count,
        "active_count": active_count,
        "inactive_count": inactive_count,
        "total_movements": total_movements,
        "most_active_user": most_active_user,
        "rows": rows,
    }


def _delete_user(user_id: int):
    with get_session() as session:
        try:
            user_service.delete_user(session, user_id)
            ui.notify("User deleted successfully", color="green")
            ui.navigate.to("/users")
        except Exception as e:
            ui.notify(str(e), color="red")


def _change_role_dialog(user_id: int):
    with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
        ui.label("Change User Role").classes("text-xl font-semibold")

        role_select = ui.select(
            ["admin", "staff"],
            value="staff",
            label="Select new role",
        ).classes("w-full")

        def save_role():
            with get_session() as session:
                try:
                    user_service.change_role(
                        session,
                        user_id,
                        role_select.value,
                    )
                    ui.notify("Role updated successfully", color="green")
                    dialog.close()
                    ui.navigate.to("/users")
                except Exception as e:
                    ui.notify(str(e), color="red")

        with ui.row().classes("justify-end w-full mt-4"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Save", on_click=save_role).props("color=primary")

    dialog.open()


def _reset_password_dialog(user_id: int):
    with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
        ui.label("Reset Password").classes("text-xl font-semibold")

        password_input = ui.input(
            "New password",
            password=True,
            password_toggle_button=True,
        ).classes("w-full")

        def save_password():
            password = str(password_input.value or "").strip()

            if not password:
                ui.notify("Please enter a new password.", color="orange")
                return

            password_hash = hashlib.sha256(
                password.encode()
            ).hexdigest()

            with get_session() as session:
                try:
                    user_service.update_user(
                        session,
                        user_id,
                        {"password_hash": password_hash},
                    )
                    ui.notify("Password reset successfully", color="green")
                    dialog.close()
                    ui.navigate.to("/users")
                except Exception as e:
                    ui.notify(str(e), color="red")

        with ui.row().classes("justify-end w-full mt-4"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Save", on_click=save_password).props("color=primary")

    dialog.open()


def _add_user_dialog():
    with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
        ui.label("Add New User").classes("text-xl font-semibold")

        name_input = ui.input("Username").classes("w-full")

        password_input = ui.input(
            "Password",
            password=True,
            password_toggle_button=True,
        ).classes("w-full")

        role_select = ui.select(
            ["admin", "staff"],
            value="staff",
            label="Role",
        ).classes("w-full")

        def create_user():
            name = str(name_input.value or "").strip()
            password = str(password_input.value or "").strip()
            role = role_select.value

            if not name:
                ui.notify("Please enter a username.", color="orange")
                return

            if not password:
                ui.notify("Please enter a password.", color="orange")
                return

            password_hash = hashlib.sha256(
                password.encode()
            ).hexdigest()

            new_user = User(
                name=name,
                role=role,
                password_hash=password_hash,
            )

            with get_session() as session:
                try:
                    session.add(new_user)
                    session.commit()
                    ui.notify("User created successfully", color="green")
                    dialog.close()
                    ui.navigate.to("/users")
                except Exception as e:
                    ui.notify(str(e), color="red")

        with ui.row().classes("justify-end w-full mt-4"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Create", on_click=create_user).props("color=primary")

    dialog.open()


def _stat_card(title: str, value: str, icon: str, icon_color: str):
    with ui.card().classes(
        "rounded-2xl shadow-sm px-4 py-3 bg-white min-w-[160px] flex-1"
    ):
        with ui.row().classes("items-center gap-3"):
            ui.icon(icon).classes(f"text-2xl {icon_color}")
            with ui.column().classes("gap-0"):
                ui.label(value).classes(
                    "text-xl font-bold text-[#0f172a] leading-none"
                )
                ui.label(title).classes("text-xs text-[#667085]")


@ui.page("/users")
def users_page() -> None:
    role = _get_user_role()
    is_admin = role == "admin"
    data = _load_user_data()

    current_name = current_user.get("name") or "Unknown"
    current_role = current_user.get("role") or "Unknown"

    ui.add_css("""
    .q-table tbody tr:hover {
        background-color: #f5f8ff;
        transition: 0.2s;
    }
    """)

    def content() -> None:
        with ui.row().classes("w-full gap-3 flex-wrap"):
            _stat_card("Total Users", str(data["total_users"]), "group", "text-[#6fa1d8]")
            _stat_card("Active Users", str(data["active_count"]), "check_circle", "text-green-500")
            _stat_card("Inactive Users", str(data["inactive_count"]), "cancel", "text-orange-500")
            _stat_card("Admins", str(data["admin_count"]), "admin_panel_settings", "text-[#6fa1d8]")
            _stat_card("Staff", str(data["staff_count"]), "badge", "text-[#6fa1d8]")
            _stat_card("Total Movements", str(data["total_movements"]), "swap_horiz", "text-[#6fa1d8]")

        with ui.card().classes("w-full rounded-3xl p-6 shadow-sm"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("gap-0"):
                    ui.label("All Users").classes("text-xl font-semibold text-gray-900")
                    ui.label("Overview of application users and their activity.").classes("text-sm text-gray-500")

                if is_admin:
                    ui.button(
                        "+ Add User",
                        on_click=_add_user_dialog,
                    ).props("color=primary").classes(
                        "rounded-xl px-4 py-2 shadow-sm"
                    )

            ui.separator().classes("my-4")

            if not data["rows"]:
                ui.label("No users found.").classes("text-base text-gray-500")
                return

            search = ui.input(
                "Search users",
                placeholder="Search by name, role or status...",
            ).props("clearable outlined dense").classes("w-full mb-4")

            columns = [
                {"name": "user_id", "label": "ID", "field": "user_id", "align": "left"},
                {"name": "name", "label": "Name", "field": "name", "align": "left"},
                {"name": "role", "label": "Role", "field": "role", "align": "left"},
                {"name": "movements", "label": "Movements", "field": "movements", "align": "left"},
                {"name": "status", "label": "Status", "field": "status", "align": "left"},
            ]

            if is_admin:
                columns.append({
                    "name": "actions",
                    "label": "Actions",
                    "field": "actions",
                    "align": "left",
                })

            table = ui.table(
                columns=columns,
                rows=data["rows"],
                row_key="user_id",
            ).classes("w-full rounded-xl overflow-hidden")

            search.bind_value(table, "filter")

            table.add_slot(
                "body-cell-role",
                """
                <q-td :props="props">
                    <q-badge
                        :color="props.row.role === 'admin' ? 'blue' : 'grey'"
                        rounded
                        class="px-3 py-1"
                    >
                        {{ props.row.role }}
                    </q-badge>
                </q-td>
                """
            )

            table.add_slot(
                "body-cell-status",
                """
                <q-td :props="props">
                    <q-badge
                        :color="props.row.status === 'Active' ? 'green' : 'orange'"
                        rounded
                        class="px-3 py-1"
                    >
                        {{ props.row.status }}
                    </q-badge>
                </q-td>
                """
            )

            table.add_slot(
                "body-cell-movements",
                """
                <q-td :props="props">
                    <div class="row items-center no-wrap" style="gap: 10px;">
                        <span style="min-width: 28px;">
                            {{ props.row.movements }}
                        </span>
                        <q-linear-progress
                            :value="Math.min(props.row.movements / 10, 1)"
                            size="8px"
                            rounded
                            color="primary"
                            track-color="grey-3"
                            style="width: 100px;"
                        />
                    </div>
                </q-td>
                """
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
                            title="Change user role"
                            @click="$parent.$emit('change-role', props.row.user_id)"
                        />

                        <q-btn
                            dense
                            flat
                            icon="key"
                            color="warning"
                            title="Reset password"
                            @click="$parent.$emit('reset-password', props.row.user_id)"
                        />

                        <q-btn
                            dense
                            flat
                            icon="delete"
                            color="negative"
                            title="Delete user"
                            @click="$parent.$emit('delete-user', props.row.user_id)"
                        />
                    </q-td>
                    """
                )

                table.on("delete-user", lambda e: _delete_user(e.args))
                table.on("change-role", lambda e: _change_role_dialog(e.args))
                table.on("reset-password", lambda e: _reset_password_dialog(e.args))

        with ui.row().classes("w-full gap-6 flex-wrap"):
            with ui.card().classes(
                "flex-1 min-w-[360px] rounded-3xl p-6 shadow-sm"
            ):
                ui.label("Role Overview").classes("text-xl font-semibold text-gray-900")
                ui.label("Permission and role distribution.").classes("text-sm text-gray-500 mb-4")

                total = data["total_users"] or 1
                admin_percent = round((data["admin_count"] / total) * 100)
                staff_percent = round((data["staff_count"] / total) * 100)

                ui.label(f"Admins: {data['admin_count']} ({admin_percent}%)").classes(
                    "font-semibold text-blue-600"
                )
                ui.linear_progress(admin_percent / 100).classes("w-full mb-3")

                ui.label(f"Staff: {data['staff_count']} ({staff_percent}%)").classes(
                    "font-semibold text-gray-600"
                )
                ui.linear_progress(staff_percent / 100).classes("w-full mb-4")

                ui.separator()

                ui.label("Admin").classes("font-semibold text-blue-600 mt-3")
                ui.label("Can manage users, locations, products, passwords and reports.").classes(
                    "text-sm text-gray-600"
                )

                ui.label("Staff").classes("font-semibold text-gray-600 mt-3")
                ui.label("Can view inventory and work with operational functions.").classes(
                    "text-sm text-gray-600"
                )

            with ui.card().classes(
                "flex-1 min-w-[360px] rounded-3xl p-6 shadow-sm"
            ):
                ui.label("User Activity").classes("text-xl font-semibold text-gray-900")
                ui.label("Overview of current user activity.").classes("text-sm text-gray-500 mb-4")

                most_active = data["most_active_user"]

                if most_active:
                    ui.label("Most Active User").classes("text-sm text-gray-500")
                    ui.label(
                        f"{most_active['name']} — {most_active['movements']} movements"
                    ).classes("text-lg font-semibold text-[#0f172a] mb-3")

                ui.label("Current Session").classes("text-sm text-gray-500")
                ui.label(
                    f"{current_name} ({current_role})"
                ).classes("text-lg font-semibold text-[#0f172a] mb-3")

                ui.label("Total Movements").classes("text-sm text-gray-500")
                ui.label(
                    str(data["total_movements"])
                ).classes("text-2xl font-bold text-[#0f172a] mb-3")

                ui.label("Inactive Users").classes("text-sm text-gray-500")
                ui.label(
                    str(data["inactive_count"])
                ).classes("text-lg font-semibold text-orange-500")

    render_shell(
        title="Users",
        subtitle="View application users and usage counts.",
        active_route="/users",
        content_builder=content,
    )